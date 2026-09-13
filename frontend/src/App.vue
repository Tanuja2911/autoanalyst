<template>
  <div class="min-h-screen bg-dark text-text">
    <!-- Header -->
    <header class="border-b border-border/60 bg-dark/90 backdrop-blur-xl px-5 py-2.5 flex items-center justify-between sticky top-0 z-50">
      <div class="flex items-center gap-2.5">
        <div class="w-7 h-7 rounded-lg bg-gradient-to-br from-primary to-accent-pink flex items-center justify-center shadow-lg shadow-primary/20">
          <svg class="w-3.5 h-3.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 3v11.25A2.25 2.25 0 006 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0118 16.5h-2.25m-7.5 0h7.5m-7.5 0l-1 3m8.5-3l1 3m0 0l.5 1.5m-.5-1.5h-9.5m0 0l-.5 1.5" />
          </svg>
        </div>
        <h1 class="text-sm font-bold text-white tracking-tight">
          <span class="text-primary">Auto</span>Analyst
        </h1>
      </div>

      <div class="flex items-center gap-2.5">
        <div v-if="fileInfo" class="flex items-center gap-2 px-2.5 py-1 bg-accent-green/8 border border-accent-green/15 rounded-lg">
          <span class="w-1.5 h-1.5 rounded-full bg-accent-green animate-pulse"></span>
          <span class="text-[11px] text-accent-green font-medium">{{ fileInfo.filename }}</span>
        </div>
        <div class="text-[10px] text-muted/50 font-medium tracking-wider">v1.0</div>
      </div>
    </header>

    <FileUpload v-if="!fileInfo" @uploaded="onFileUploaded" />
    <AnalysisView v-else :file-info="fileInfo" @reset="fileInfo = null" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import FileUpload from './components/FileUpload.vue'
import AnalysisView from './components/AnalysisView.vue'

const fileInfo = ref(null)

function onFileUploaded(info) {
  fileInfo.value = info
}
</script>
