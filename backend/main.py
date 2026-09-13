import os
import json
import re
import uuid

import pandas as pd
from fastapi import FastAPI, WebSocket, UploadFile, File, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

from agent import build_agent

load_dotenv()

app = FastAPI(title="AutoAnalyst")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
datasets = {}


def extract_charts(text):
    charts = []
    match = re.search(r'\[CHARTS\](.*?)\[/CHARTS\]', text, re.DOTALL)
    if match:
        try:
            charts = json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    clean_text = re.sub(r'\[CHARTS\].*?\[/CHARTS\]', '', text, flags=re.DOTALL).strip()
    return clean_text, charts


def get_text(content):
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block["text"])
            elif isinstance(block, str):
                parts.append(block)
        return "\n".join(parts)
    return str(content) if content else ""


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        return JSONResponse(status_code=400, content={"error": "Only CSV files supported"})

    content = await file.read()
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(content)

    try:
        df = pd.read_csv(file_path)
        file_id = file.filename.rsplit('.', 1)[0]
        datasets[file_id] = df
        return {
            "file_id": file_id,
            "filename": file.filename,
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": list(df.columns)
        }
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


@app.get("/preview/{file_id}")
async def preview_data(file_id: str):
    df = datasets.get(file_id)
    if df is None:
        return JSONResponse(status_code=404, content={"error": "Dataset not found"})
    preview = df.head(5).fillna("").to_dict(orient="records")
    return {"rows": preview}


@app.websocket("/ws/analyze/{file_id}")
async def analyze(websocket: WebSocket, file_id: str):
    await websocket.accept()

    df = datasets.get(file_id)
    if df is None:
        await websocket.send_json({"type": "error", "content": "Dataset not found. Please upload first."})
        await websocket.close()
        return

    agent = build_agent(df, GOOGLE_API_KEY)
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}, "recursion_limit": 12}

    try:
        while True:
            data = await websocket.receive_json()
            query = data.get("query", "Analyze this dataset thoroughly")

            await websocket.send_json({"type": "status", "content": "Agent is thinking..."})

            try:
                async for event in agent.astream(
                    {"messages": [HumanMessage(content=query)]},
                    config=config,
                    stream_mode="updates",
                ):
                    for node_name, node_data in event.items():
                        for msg in node_data.get("messages", []):
                            if isinstance(msg, AIMessage):
                                if msg.tool_calls:
                                    for tc in msg.tool_calls:
                                        await websocket.send_json({
                                            "type": "thought",
                                            "content": f"Using tool: {tc['name']}"
                                        })
                                        if tc["name"] == "python_repl":
                                            code = tc.get("args", {}).get("code", "")
                                            if code:
                                                await websocket.send_json({
                                                    "type": "code",
                                                    "content": code
                                                })

                                content = get_text(msg.content)
                                if content.strip() and not msg.tool_calls:
                                    await websocket.send_json({
                                        "type": "thought",
                                        "content": "Generating final report..."
                                    })
                                    await websocket.send_json({
                                        "type": "answer",
                                        "content": content
                                    })

                            elif isinstance(msg, ToolMessage):
                                raw = get_text(msg.content)
                                clean_text, charts = extract_charts(raw)

                                for img in charts:
                                    await websocket.send_json({
                                        "type": "chart",
                                        "image": img
                                    })

                                if clean_text:
                                    await websocket.send_json({
                                        "type": "output",
                                        "content": clean_text[:3000]
                                    })

            except Exception as e:
                await websocket.send_json({"type": "error", "content": str(e)})

    except WebSocketDisconnect:
        pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
