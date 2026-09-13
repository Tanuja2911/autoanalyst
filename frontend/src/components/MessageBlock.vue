<template>
  <div class="animate-fade-in">
    <!-- User message -->
    <div v-if="message.type === 'user'" class="flex justify-end">
      <div class="bg-primary/12 border border-primary/20 rounded-2xl rounded-br-md px-4 py-2.5 max-w-2xl">
        <p class="text-sm text-white leading-relaxed">{{ message.content }}</p>
      </div>
    </div>

    <!-- Status -->
    <div v-else-if="message.type === 'status'" class="flex items-center gap-2.5 py-1.5">
      <div class="w-5 h-5 rounded-full bg-accent-cyan/10 flex items-center justify-center">
        <svg class="w-2.5 h-2.5 text-accent-cyan animate-spin" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
        </svg>
      </div>
      <p class="text-xs text-accent-cyan font-medium">{{ message.content }}</p>
    </div>

    <!-- Thought (tool being used) -->
    <div v-else-if="message.type === 'thought'" class="flex items-center gap-2.5 py-1.5">
      <div class="w-5 h-5 rounded-full bg-primary/12 flex items-center justify-center flex-shrink-0">
        <svg class="w-2.5 h-2.5 text-primary" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd"/>
        </svg>
      </div>
      <p class="text-xs text-primary-light font-medium tracking-wide">{{ message.content }}</p>
    </div>

    <!-- Code block -->
    <div v-else-if="message.type === 'code'" class="ml-7">
      <div class="bg-[#08080f] border border-border rounded-xl overflow-hidden">
        <div class="flex items-center justify-between px-4 py-2 border-b border-border bg-[#0a0a14]">
          <div class="flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full bg-accent-green/60"></span>
            <span class="text-[10px] text-muted font-mono tracking-wider uppercase">Python</span>
          </div>
          <button @click="copyCode(message.content)" class="text-[10px] text-muted hover:text-white transition">
            {{ copied ? 'Copied!' : 'Copy' }}
          </button>
        </div>
        <pre class="p-4 overflow-x-auto max-h-72"><code class="text-[12px] leading-5 text-green-300 whitespace-pre" style="font-family: 'JetBrains Mono', monospace">{{ message.content }}</code></pre>
      </div>
    </div>

    <!-- Output -->
    <div v-else-if="message.type === 'output'" class="ml-7">
      <details class="group">
        <summary class="text-[11px] text-muted cursor-pointer hover:text-text transition flex items-center gap-1.5 py-1.5 font-medium">
          <svg class="w-3 h-3 transition-transform duration-200 group-open:rotate-90" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
          </svg>
          Output
          <span class="text-[10px] text-muted/50 ml-1">(click to expand)</span>
        </summary>
        <pre class="bg-surface border border-border rounded-xl p-3 overflow-x-auto max-h-52 mt-1.5"><code class="text-[11px] leading-4 text-muted whitespace-pre" style="font-family: 'JetBrains Mono', monospace">{{ message.content }}</code></pre>
      </details>
    </div>

    <!-- Chart -->
    <div v-else-if="message.type === 'chart'" class="ml-7 py-2">
      <div class="rounded-xl border border-border overflow-hidden bg-surface-card inline-block shadow-xl shadow-black/20">
        <img
          :src="'data:image/png;base64,' + message.image"
          class="max-w-full"
          alt="Generated chart"
        />
      </div>
    </div>

    <!-- Final answer -->
    <div v-else-if="message.type === 'answer'" class="mt-5">
      <div class="bg-surface-card/80 border border-primary/15 rounded-2xl overflow-hidden">
        <div class="flex items-center gap-2 px-5 py-3 bg-accent-green/5 border-b border-border">
          <div class="w-5 h-5 rounded-full bg-accent-green/15 flex items-center justify-center">
            <svg class="w-3 h-3 text-accent-green" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
            </svg>
          </div>
          <span class="text-xs font-semibold text-accent-green uppercase tracking-wider">Analysis Complete</span>
        </div>
        <div class="px-5 py-4 text-[13px] text-text leading-relaxed markdown-body" v-html="renderMarkdown(message.content)"></div>
      </div>
    </div>

    <!-- Error -->
    <div v-else-if="message.type === 'error'" class="py-1.5">
      <div class="bg-accent-pink/8 border border-accent-pink/20 rounded-xl px-4 py-3 flex items-center gap-2.5">
        <svg class="w-4 h-4 text-accent-pink flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
        </svg>
        <p class="text-sm text-accent-pink">{{ message.content }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  message: { type: Object, required: true }
})

const copied = ref(false)

function copyCode(code) {
  navigator.clipboard.writeText(code)
  copied.value = true
  setTimeout(() => { copied.value = false }, 2000)
}

function renderMarkdown(text) {
  if (!text) return ''
  return text
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^# (.+)$/gm, '<h1>$1</h1>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/`(.+?)`/g, '<code>$1</code>')
    .replace(/^---$/gm, '<hr>')
    .replace(/^\* (.+)$/gm, '<li>$1</li>')
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    .replace(/^(\d+)\. (.+)$/gm, '<li>$2</li>')
    .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
    .replace(/\n{2,}/g, '</p><p>')
    .replace(/\n/g, '<br>')
    .replace(/^\|(.+)\|$/gm, (match) => {
      const cells = match.split('|').filter(c => c.trim())
      if (cells.every(c => /^[\s:-]+$/.test(c))) return ''
      const tag = match.includes('---') ? 'th' : 'td'
      return '<tr>' + cells.map(c => `<${tag}>${c.trim()}</${tag}>`).join('') + '</tr>'
    })
    .replace(/(<tr>.*<\/tr>)/s, '<table>$1</table>')
}
</script>
