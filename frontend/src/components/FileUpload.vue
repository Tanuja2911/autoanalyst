<template>
  <div class="flex items-center justify-center min-h-[calc(100vh-48px)] px-6 relative overflow-hidden">
    <!-- Background glow -->
    <div class="absolute top-1/4 left-1/2 -translate-x-1/2 w-[500px] h-[500px] bg-primary/5 rounded-full blur-[120px] pointer-events-none"></div>

    <div class="w-full max-w-lg animate-slide-up relative z-10">
      <!-- Hero -->
      <div class="text-center mb-8">
        <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-primary/8 border border-primary/15 mb-5">
          <svg class="w-3 h-3 text-primary" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd"/>
          </svg>
          <span class="text-[11px] text-primary-light font-semibold tracking-wide">AI-POWERED ANALYSIS</span>
        </div>
        <h2 class="text-3xl font-bold tracking-tight mb-3">
          <span class="text-white">Analyze any </span>
          <span class="bg-gradient-to-r from-primary to-accent-cyan bg-clip-text text-transparent">dataset</span>
        </h2>
        <p class="text-sm text-muted max-w-md mx-auto leading-relaxed">
          Upload a CSV and get instant charts, correlations, and AI-powered insights in seconds
        </p>
      </div>

      <!-- Upload zone -->
      <div
        class="border border-dashed rounded-2xl p-8 text-center transition-all duration-300 cursor-pointer relative group"
        :class="dragging
          ? 'border-primary bg-primary/6 shadow-xl shadow-primary/10'
          : 'border-border/60 hover:border-primary/30 hover:bg-surface-card/30'"
        @dragover.prevent="dragging = true"
        @dragleave="dragging = false"
        @drop.prevent="onDrop"
        @click="$refs.fileInput.click()"
      >
        <input ref="fileInput" type="file" accept=".csv" class="hidden" @change="onFileSelect" />

        <div v-if="!uploading" class="space-y-4">
          <div class="w-14 h-14 mx-auto rounded-xl bg-surface-card border border-border/60 flex items-center justify-center group-hover:border-primary/30 group-hover:shadow-lg group-hover:shadow-primary/5 transition-all" :class="dragging ? 'animate-pulse-glow border-primary/40' : ''">
            <svg class="w-6 h-6 text-muted group-hover:text-primary transition" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
            </svg>
          </div>
          <div>
            <p class="text-white font-semibold text-sm">Drop your CSV file here</p>
            <p class="text-xs text-muted mt-1">or click to browse</p>
          </div>
        </div>

        <div v-else class="space-y-4 py-2">
          <div class="w-14 h-14 mx-auto rounded-xl bg-primary/10 flex items-center justify-center animate-pulse-glow">
            <svg class="w-6 h-6 text-primary animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
          </div>
          <p class="text-muted text-xs font-medium">Processing your file...</p>
        </div>

        <p v-if="error" class="text-accent-pink text-xs mt-3 font-medium">{{ error }}</p>
      </div>

      <!-- Feature cards -->
      <div class="grid grid-cols-4 gap-2.5 mt-6">
        <div class="bg-surface-card/50 border border-border/40 rounded-xl px-2.5 py-3 text-center">
          <div class="w-7 h-7 mx-auto rounded-lg bg-primary/8 flex items-center justify-center mb-1.5">
            <svg class="w-3.5 h-3.5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" />
            </svg>
          </div>
          <p class="text-[10px] font-semibold text-white">Auto Charts</p>
          <p class="text-[9px] text-muted mt-0.5">Visualizations</p>
        </div>
        <div class="bg-surface-card/50 border border-border/40 rounded-xl px-2.5 py-3 text-center">
          <div class="w-7 h-7 mx-auto rounded-lg bg-accent-cyan/8 flex items-center justify-center mb-1.5">
            <svg class="w-3.5 h-3.5 text-accent-cyan" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M7.5 14.25v2.25m3-4.5v4.5m3-6.75v6.75m3-9v9M6 20.25h12A2.25 2.25 0 0020.25 18V6A2.25 2.25 0 0018 3.75H6A2.25 2.25 0 003.75 6v12A2.25 2.25 0 006 20.25z" />
            </svg>
          </div>
          <p class="text-[10px] font-semibold text-white">Correlations</p>
          <p class="text-[9px] text-muted mt-0.5">Patterns</p>
        </div>
        <div class="bg-surface-card/50 border border-border/40 rounded-xl px-2.5 py-3 text-center">
          <div class="w-7 h-7 mx-auto rounded-lg bg-accent-green/8 flex items-center justify-center mb-1.5">
            <svg class="w-3.5 h-3.5 text-accent-green" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.455 2.456L21.75 6l-1.036.259a3.375 3.375 0 00-2.455 2.456z" />
            </svg>
          </div>
          <p class="text-[10px] font-semibold text-white">AI Insights</p>
          <p class="text-[9px] text-muted mt-0.5">LLM-powered</p>
        </div>
        <div class="bg-surface-card/50 border border-border/40 rounded-xl px-2.5 py-3 text-center">
          <div class="w-7 h-7 mx-auto rounded-lg bg-accent-pink/8 flex items-center justify-center mb-1.5">
            <svg class="w-3.5 h-3.5 text-accent-pink" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
            </svg>
          </div>
          <p class="text-[10px] font-semibold text-white">Export</p>
          <p class="text-[9px] text-muted mt-0.5">Download all</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['uploaded'])

const dragging = ref(false)
const uploading = ref(false)
const error = ref('')

async function uploadFile(file) {
  if (!file || !file.name.endsWith('.csv')) {
    error.value = 'Please upload a CSV file'
    return
  }

  uploading.value = true
  error.value = ''

  const formData = new FormData()
  formData.append('file', file)

  try {
    const res = await fetch('http://localhost:8000/upload', {
      method: 'POST',
      body: formData
    })

    if (!res.ok) {
      const data = await res.json()
      throw new Error(data.error || 'Upload failed')
    }

    const data = await res.json()
    emit('uploaded', data)
  } catch (e) {
    error.value = e.message
  } finally {
    uploading.value = false
  }
}

function onFileSelect(e) {
  uploadFile(e.target.files[0])
}

function onDrop(e) {
  dragging.value = false
  uploadFile(e.dataTransfer.files[0])
}
</script>
