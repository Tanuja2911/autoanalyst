import io
import sys
import json
import base64

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver


SYSTEM_PROMPT = """You are AutoAnalyst, an autonomous data analysis agent. You analyze datasets by deciding which tools to use and what code to write.

TOOLS:
- data_preview: Dataset overview (shape, columns, types, sample rows, stats)
- python_repl: Execute Python code. Variables persist across calls. Available: df, pd, np, plt, sns.

WORKFLOW:
1. Call data_preview to understand the dataset
2. Call python_repl to compute key statistics (correlations, group-by, value counts) — do ALL stats in ONE call
3. Call python_repl to create ALL visualizations in ONE call (use subplots)
4. Give your final answer

BE EFFICIENT: Combine related computations into a single python_repl call. Aim for 3-4 total tool calls, not 8-10.

CHART STYLING:
- plt.style.use('dark_background')
- fig.patch.set_facecolor('#1a1a2e'); ax.set_facecolor('#1a1a2e')
- colors = ['#7c5cfc', '#5cf0fc', '#fc5c7c', '#5cfc7c', '#fcb45c']
- plt.tight_layout(); Do NOT call plt.show()
- Use figsize=(14, 10) for multi-chart subplots

You are an autonomous AGENT — you decide what to analyze and what code to write. Think step by step, then act.

Format your final answer in markdown with key findings, patterns, anomalies, and recommendations."""


def create_tools(df):
    exec_namespace = {
        "df": df, "pd": pd, "np": np,
        "plt": plt, "sns": sns,
        "io": io, "base64": base64,
    }

    @tool
    def data_preview() -> str:
        """Get an overview of the dataset: shape, columns with data types, first 5 rows, missing values, and descriptive statistics. Always call this first to understand the data before doing any analysis."""
        result = f"Shape: {df.shape[0]} rows x {df.shape[1]} columns\n\n"
        result += "Columns:\n"
        for col in df.columns:
            nunique = df[col].nunique()
            result += f"  - {col} ({df[col].dtype}, {nunique} unique)\n"
        result += f"\nFirst 5 rows:\n{df.head().to_string()}\n\n"
        result += f"Missing values:\n{df.isnull().sum().to_string()}\n\n"
        result += f"Statistics:\n{df.describe(include='all').to_string()}"
        return result

    @tool
    def python_repl(code: str) -> str:
        """Execute Python code for data analysis. The dataset is available as 'df' (pandas DataFrame).
        Available: pandas (pd), numpy (np), matplotlib.pyplot (plt), seaborn (sns).
        Use print() to display computed results. Charts are automatically captured.
        Variables persist across calls — you can define a variable in one call and use it in the next."""
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        plt.close('all')

        try:
            exec(code, {"__builtins__": __builtins__}, exec_namespace)
            output = sys.stdout.getvalue()

            charts = []
            for fig_num in plt.get_fignums():
                fig = plt.figure(fig_num)
                fig.patch.set_facecolor('#1a1a2e')
                for ax in fig.get_axes():
                    ax.set_facecolor('#1a1a2e')
                buf = io.BytesIO()
                fig.savefig(buf, format='png', bbox_inches='tight', dpi=150,
                            facecolor='#1a1a2e', edgecolor='none')
                buf.seek(0)
                charts.append(base64.b64encode(buf.read()).decode())
                plt.close(fig)

            result = output.strip() if output.strip() else "Code executed successfully."
            if charts:
                result += f"\n[CHARTS]{json.dumps(charts)}[/CHARTS]"
            return result
        except Exception as e:
            return f"Error: {type(e).__name__}: {str(e)}"
        finally:
            sys.stdout = old_stdout
            plt.close('all')

    return [data_preview, python_repl]


def build_agent(df, api_key):
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        google_api_key=api_key,
    )
    tools = create_tools(df)
    memory = MemorySaver()

    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=SYSTEM_PROMPT,
        checkpointer=memory,
    )

    return agent
