<template>
  <div class="flex h-[calc(100vh-48px)]">
    <!-- Left Sidebar: Agent Activity -->
    <div
      class="border-r border-border/50 bg-surface/40 flex flex-col transition-all duration-300 relative"
      :class="sidebarOpen ? 'w-72' : 'w-0 overflow-hidden'"
    >
      <!-- Sidebar header -->
      <div class="flex items-center justify-between px-3.5 py-2.5 border-b border-border/50">
        <div class="flex items-center gap-2">
          <div class="w-5 h-5 rounded-md bg-primary/12 flex items-center justify-center">
            <svg class="w-3 h-3 text-primary" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd"/>
            </svg>
          </div>
          <span class="text-[11px] font-semibold text-muted tracking-wide uppercase">Activity</span>
        </div>
        <span v-if="currentActivity.length" class="text-[10px] text-muted/60 font-mono">{{ currentActivity.length }}</span>
      </div>

      <!-- Progress stepper -->
      <div v-if="loading || currentRoundComplete" class="px-3 py-2.5 border-b border-border/30">
        <div class="flex items-center gap-1">
          <div v-for="(step, i) in analysisSteps" :key="i" class="flex items-center gap-1 flex-1">
            <div
              class="w-5 h-5 rounded-full flex items-center justify-center text-[9px] font-bold transition-all duration-300 flex-shrink-0"
              :class="step.done ? 'bg-accent-green/20 text-accent-green' : step.active ? 'bg-primary/20 text-primary animate-pulse' : 'bg-border/20 text-muted/30'"
            >
              <svg v-if="step.done" class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
              </svg>
              <span v-else>{{ i + 1 }}</span>
            </div>
            <div v-if="i < analysisSteps.length - 1" class="flex-1 h-px transition-all duration-300" :class="step.done ? 'bg-accent-green/30' : 'bg-border/20'"></div>
          </div>
        </div>
        <div class="flex justify-between mt-1.5">
          <span v-for="(step, i) in analysisSteps" :key="'l'+i" class="text-[8px] tracking-wide" :class="step.done ? 'text-accent-green/60' : step.active ? 'text-primary/60' : 'text-muted/20'">{{ step.label }}</span>
        </div>
      </div>

      <!-- Activity feed -->
      <div ref="sidebarScroll" class="flex-1 overflow-y-auto px-2 py-2 space-y-0.5">
        <div v-if="currentActivity.length === 0 && !loading" class="flex flex-col items-center justify-center py-12 text-center px-4">
          <div class="w-8 h-8 rounded-lg bg-border/30 flex items-center justify-center mb-3">
            <svg class="w-4 h-4 text-muted/40" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <p class="text-[11px] text-muted/50">Waiting for analysis</p>
        </div>

        <template v-for="(msg, i) in currentActivity" :key="i">
          <div v-if="msg.type === 'status'" class="flex items-center gap-2 py-1.5 px-2.5 animate-fade-in">
            <div class="w-4 h-4 rounded-full bg-accent-cyan/10 flex items-center justify-center flex-shrink-0">
              <svg class="w-2.5 h-2.5 text-accent-cyan animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
            </div>
            <p class="text-[11px] text-accent-cyan font-medium truncate">{{ msg.content }}</p>
          </div>
          <div v-else-if="msg.type === 'thought'" class="flex items-center gap-2 py-1.5 px-2.5 rounded-lg hover:bg-surface-hover/40 transition animate-fade-in">
            <div class="w-4 h-4 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
              <div class="w-1.5 h-1.5 rounded-full bg-primary"></div>
            </div>
            <p class="text-[11px] text-primary-light/80 font-medium truncate">{{ msg.content }}</p>
          </div>
          <div v-else-if="msg.type === 'code'" class="animate-fade-in px-1">
            <details class="group">
              <summary class="flex items-center gap-2 py-1.5 px-1.5 rounded-lg cursor-pointer hover:bg-surface-hover/40 transition">
                <div class="w-4 h-4 rounded-full bg-accent-green/10 flex items-center justify-center flex-shrink-0">
                  <svg class="w-2.5 h-2.5 text-accent-green transition-transform group-open:rotate-90" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
                  </svg>
                </div>
                <span class="text-[11px] text-accent-green/70 font-medium">Code executed</span>
              </summary>
              <pre class="bg-dark/80 border border-border/40 rounded-lg p-2 mt-1 overflow-x-auto max-h-32"><code class="text-[10px] leading-4 text-accent-green/60 whitespace-pre" style="font-family: 'JetBrains Mono', monospace">{{ msg.content }}</code></pre>
            </details>
          </div>
          <div v-else-if="msg.type === 'output'" class="animate-fade-in px-1">
            <details class="group">
              <summary class="flex items-center gap-2 py-1.5 px-1.5 rounded-lg cursor-pointer hover:bg-surface-hover/40 transition">
                <div class="w-4 h-4 rounded-full bg-muted/10 flex items-center justify-center flex-shrink-0">
                  <svg class="w-2.5 h-2.5 text-muted/50 transition-transform group-open:rotate-90" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
                  </svg>
                </div>
                <span class="text-[11px] text-muted/50 font-medium">Output</span>
              </summary>
              <pre class="bg-dark/60 border border-border/30 rounded-lg p-2 mt-1 overflow-x-auto max-h-28"><code class="text-[10px] leading-4 text-muted/60 whitespace-pre" style="font-family: 'JetBrains Mono', monospace">{{ msg.content }}</code></pre>
            </details>
          </div>
        </template>

        <div v-if="loading" class="flex items-center gap-2 py-2 px-2.5 animate-fade-in">
          <div class="flex gap-0.5">
            <span class="w-1 h-1 bg-primary/50 rounded-full typing-dot"></span>
            <span class="w-1 h-1 bg-primary/50 rounded-full typing-dot"></span>
            <span class="w-1 h-1 bg-primary/50 rounded-full typing-dot"></span>
          </div>
          <span class="text-[10px] text-muted/40">Working...</span>
        </div>
      </div>

      <!-- Timer -->
      <div v-if="loading || analysisTime" class="px-3.5 py-2 border-t border-border/30 flex items-center justify-between">
        <span class="text-[10px] text-muted/40">Duration</span>
        <span class="text-[11px] font-mono" :class="loading ? 'text-primary/60' : 'text-accent-green/60'">{{ formattedTime }}</span>
      </div>
    </div>

    <!-- Main Dashboard Area -->
    <div class="flex-1 flex flex-col min-w-0">
      <!-- Top bar -->
      <div class="flex items-center justify-between px-5 py-2 border-b border-border/40 bg-dark/60">
        <div class="flex items-center gap-2">
          <button
            @click="sidebarOpen = !sidebarOpen"
            class="w-7 h-7 rounded-lg border border-border/50 flex items-center justify-center text-muted hover:text-white hover:border-border transition mr-1"
          >
            <svg class="w-3.5 h-3.5 transition-transform duration-300" :class="sidebarOpen ? '' : 'rotate-180'" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25H12" />
            </svg>
          </button>
          <div class="flex items-center gap-1.5">
            <div class="flex items-center gap-1.5 px-2.5 py-1 bg-surface-card/60 border border-border/30 rounded-lg">
              <span class="text-[11px] text-white font-semibold">{{ fileInfo.rows.toLocaleString() }}</span>
              <span class="text-[10px] text-muted">rows</span>
            </div>
            <div class="flex items-center gap-1.5 px-2.5 py-1 bg-surface-card/60 border border-border/30 rounded-lg">
              <span class="text-[11px] text-white font-semibold">{{ fileInfo.columns }}</span>
              <span class="text-[10px] text-muted">cols</span>
            </div>
          </div>
          <div class="hidden lg:flex items-center gap-1 ml-1">
            <span v-for="col in fileInfo.column_names.slice(0, 5)" :key="col" class="text-[10px] text-muted/50 px-1.5 py-0.5 rounded bg-surface-card/30">{{ col }}</span>
            <span v-if="fileInfo.column_names.length > 5" class="text-[10px] text-muted/30">+{{ fileInfo.column_names.length - 5 }}</span>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <button
            @click="showDataPreview = !showDataPreview"
            class="text-[11px] text-muted hover:text-primary-light transition flex items-center gap-1.5 px-2.5 py-1 rounded-lg hover:bg-primary/5 border border-transparent hover:border-primary/15"
            :class="showDataPreview ? 'text-primary-light bg-primary/5 border-primary/15' : ''"
          >
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
              <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            Preview
          </button>
          <button @click="$emit('reset')" class="text-[11px] text-muted hover:text-accent-pink transition flex items-center gap-1.5 px-2.5 py-1 rounded-lg hover:bg-accent-pink/5">
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
            New
          </button>
        </div>
      </div>

      <!-- Data Preview Panel -->
      <div v-if="showDataPreview" class="border-b border-border/30 bg-surface/30 animate-fade-in">
        <div class="px-5 py-3">
          <div class="flex items-center justify-between mb-2">
            <span class="text-[11px] font-semibold text-muted tracking-wide uppercase">Data Preview</span>
            <span class="text-[10px] text-muted/40">First rows from {{ fileInfo.filename }}</span>
          </div>
          <div class="overflow-x-auto rounded-lg border border-border/30">
            <table class="w-full text-[11px]">
              <thead>
                <tr class="bg-surface-card/60">
                  <th v-for="col in fileInfo.column_names" :key="col" class="px-3 py-1.5 text-left font-semibold text-primary-light/80 border-b border-border/30 whitespace-nowrap">{{ col }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, i) in dataPreviewRows" :key="i" class="hover:bg-surface-hover/30 transition">
                  <td v-for="col in fileInfo.column_names" :key="col" class="px-3 py-1 text-muted/70 border-b border-border/15 whitespace-nowrap font-mono">{{ row[col] !== undefined ? row[col] : '—' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Dashboard content -->
      <div ref="dashboardScroll" class="flex-1 overflow-y-auto">
        <!-- Empty state -->
        <div v-if="rounds.length === 0 && !loading" class="flex flex-col items-center justify-center h-full text-center px-6 animate-fade-in">
          <div class="relative mb-6">
            <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-primary/15 to-accent-cyan/10 flex items-center justify-center">
              <svg class="w-7 h-7 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 3v11.25A2.25 2.25 0 006 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0118 16.5h-2.25m-7.5 0h7.5m-7.5 0l-1 3m8.5-3l1 3m0 0l.5 1.5m-.5-1.5h-9.5m0 0l-.5 1.5" />
              </svg>
            </div>
            <div class="absolute -top-1 -right-1 w-5 h-5 rounded-full bg-accent-green/15 flex items-center justify-center">
              <svg class="w-3 h-3 text-accent-green" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
              </svg>
            </div>
          </div>
          <p class="text-white font-semibold text-sm mb-1.5">Dataset loaded</p>
          <p class="text-xs text-muted max-w-sm leading-relaxed mb-6">
            Run a full analysis, ask a question, or request a custom chart like<br>
            <span class="text-primary-light/70">"scatter plot of age vs income colored by gender"</span>
          </p>
          <div class="flex flex-wrap justify-center gap-2 max-w-lg">
            <button
              v-for="action in quickActions"
              :key="action.label"
              @click="quickQuery(action.query)"
              class="text-[11px] px-3 py-1.5 rounded-lg transition flex items-center gap-1.5"
              :class="action.primary
                ? 'bg-primary/10 border border-primary/25 text-primary-light hover:bg-primary/15 font-medium'
                : 'bg-surface-card/60 border border-border/40 text-muted hover:border-primary/25 hover:text-primary-light'"
            >
              <span v-html="action.icon"></span>
              {{ action.label }}
            </button>
          </div>
        </div>

        <!-- Conversation rounds -->
        <div v-else class="p-5 space-y-6">
          <template v-for="(round, ri) in rounds" :key="ri">
            <!-- Round separator for rounds after the first -->
            <div v-if="ri > 0" class="flex items-center gap-3 py-1">
              <div class="flex-1 h-px bg-border/20"></div>
              <span class="text-[9px] text-muted/30 font-medium tracking-wider uppercase">Follow-up {{ ri }}</span>
              <div class="flex-1 h-px bg-border/20"></div>
            </div>

            <!-- User query -->
            <div class="flex items-start gap-2 animate-fade-in">
              <div class="w-6 h-6 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0 mt-0.5">
                <svg class="w-3 h-3 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
                </svg>
              </div>
              <p class="text-sm font-medium text-white pt-0.5">{{ round.query }}</p>
            </div>

            <!-- Charts for this round -->
            <div v-if="round.charts.length > 0" class="animate-fade-in">
              <div class="flex items-center justify-between mb-3">
                <div class="flex items-center gap-2">
                  <div class="w-5 h-5 rounded-md bg-accent-cyan/10 flex items-center justify-center">
                    <svg class="w-3 h-3 text-accent-cyan" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" />
                    </svg>
                  </div>
                  <span class="text-xs font-semibold text-white">Visualizations</span>
                  <span class="text-[10px] text-muted/40 font-mono">{{ round.charts.length }}</span>
                </div>
                <button v-if="round.charts.length" @click="downloadRoundCharts(ri)" class="text-[10px] text-muted hover:text-primary-light transition flex items-center gap-1 px-2 py-1 rounded-md hover:bg-primary/5">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
                  </svg>
                  Download
                </button>
              </div>
              <div class="grid grid-cols-1 lg:grid-cols-2 gap-3">
                <div
                  v-for="(chart, ci) in round.charts"
                  :key="ci"
                  class="group rounded-xl border border-border/40 overflow-hidden bg-surface-card/50 hover:border-border transition-all duration-200 cursor-pointer"
                  @click="openChartModal(ri, ci)"
                >
                  <img :src="'data:image/png;base64,' + chart.image" class="w-full max-h-64 object-cover object-top" alt="Chart" />
                  <div class="px-3 py-1.5 border-t border-border/30 flex items-center justify-between">
                    <div class="flex items-center gap-1.5">
                      <div class="w-1.5 h-1.5 rounded-full" :class="['bg-primary', 'bg-accent-cyan', 'bg-accent-green', 'bg-accent-pink'][ci % 4]"></div>
                      <span class="text-[10px] text-muted font-medium">{{ chart.label || chartLabels[ci] || 'Chart ' + (ci + 1) }}</span>
                    </div>
                    <svg class="w-3 h-3 text-muted/30 group-hover:text-muted transition" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 3.75v4.5m0-4.5h4.5m-4.5 0L9 9M3.75 20.25v-4.5m0 4.5h4.5m-4.5 0L9 15M20.25 3.75h-4.5m4.5 0v4.5m0-4.5L15 9m5.25 11.25h-4.5m4.5 0v-4.5m0 4.5L15 15" />
                    </svg>
                  </div>
                </div>
              </div>
            </div>

            <!-- Answer for this round -->
            <div v-if="round.answer" class="animate-slide-up">
              <div class="flex items-center justify-between mb-3">
                <div class="flex items-center gap-2">
                  <div class="w-5 h-5 rounded-md bg-accent-green/10 flex items-center justify-center">
                    <svg class="w-3 h-3 text-accent-green" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.455 2.456L21.75 6l-1.036.259a3.375 3.375 0 00-2.455 2.456z" />
                    </svg>
                  </div>
                  <span class="text-xs font-semibold text-white">AI Insights</span>
                </div>
                <button @click="copyText(round.answer)" class="text-[10px] transition flex items-center gap-1 px-2 py-1 rounded-md hover:bg-primary/5" :class="copiedRound === ri ? 'text-accent-green' : 'text-muted hover:text-primary-light'">
                  <svg v-if="copiedRound !== ri" class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.666 3.888A2.25 2.25 0 0013.5 2.25h-3c-1.03 0-1.9.693-2.166 1.638m7.332 0c.055.194.084.4.084.612v0a.75.75 0 01-.75.75H9.75a.75.75 0 01-.75-.75v0c0-.212.03-.418.084-.612m7.332 0c.646.049 1.288.11 1.927.184 1.1.128 1.907 1.077 1.907 2.185V19.5a2.25 2.25 0 01-2.25 2.25H6.75A2.25 2.25 0 014.5 19.5V6.257c0-1.108.806-2.057 1.907-2.185a48.208 48.208 0 011.927-.184" />
                  </svg>
                  <svg v-else class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                  </svg>
                  {{ copiedRound === ri ? 'Copied!' : 'Copy' }}
                </button>
              </div>
              <div class="bg-surface-card/40 border border-border/30 rounded-xl p-5">
                <div class="text-[13px] text-text/90 leading-relaxed markdown-body" v-html="renderMarkdown(round.answer)"></div>
              </div>
            </div>

            <!-- Errors -->
            <div v-for="(err, ei) in round.errors" :key="'err-'+ei" class="bg-accent-pink/5 border border-accent-pink/15 rounded-xl px-4 py-3 flex items-center gap-2.5 animate-fade-in">
              <svg class="w-4 h-4 text-accent-pink flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
              </svg>
              <p class="text-xs text-accent-pink/80">{{ err }}</p>
            </div>
          </template>

          <!-- Loading shimmer for current round -->
          <div v-if="loading && currentRound && !currentRound.answer && currentRound.charts.length === 0" class="flex items-center justify-center py-16 animate-fade-in">
            <div class="text-center">
              <div class="relative w-14 h-14 mx-auto mb-4">
                <div class="absolute inset-0 rounded-xl bg-primary/10 animate-pulse-glow"></div>
                <div class="relative w-full h-full rounded-xl bg-surface-card border border-border/40 flex items-center justify-center">
                  <svg class="w-6 h-6 text-primary animate-spin" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                  </svg>
                </div>
              </div>
              <p class="text-xs text-muted font-medium">Analyzing your data...</p>
            </div>
          </div>

          <!-- Insights shimmer -->
          <div v-if="loading && currentRound && currentRound.charts.length > 0 && !currentRound.answer" class="animate-fade-in">
            <div class="flex items-center gap-2 mb-3">
              <div class="w-5 h-5 rounded-md bg-accent-green/10 flex items-center justify-center">
                <svg class="w-3 h-3 text-accent-green animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
              </div>
              <span class="text-xs font-semibold text-white">AI Insights</span>
              <span class="text-[10px] text-muted/40">generating...</span>
            </div>
            <div class="bg-surface-card/30 border border-border/20 rounded-xl p-5 shimmer-bg">
              <div class="space-y-2.5">
                <div class="h-3 bg-border/20 rounded w-3/4"></div>
                <div class="h-3 bg-border/20 rounded w-1/2"></div>
                <div class="h-3 bg-border/20 rounded w-5/6"></div>
              </div>
            </div>
          </div>

          <!-- Follow-up suggestions (only after last round is done) -->
          <div v-if="!loading && rounds.length > 0 && lastRoundComplete" class="animate-fade-in pt-2">
            <div class="flex flex-wrap gap-2">
              <button
                v-for="action in followUpActions"
                :key="action.label"
                @click="quickQuery(action.query)"
                class="text-[11px] px-3 py-1.5 rounded-lg bg-surface-card/50 border border-border/30 text-muted hover:border-primary/25 hover:text-primary-light transition flex items-center gap-1.5"
              >
                <span v-html="action.icon"></span>
                {{ action.label }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Input bar -->
      <div class="border-t border-border/40 px-4 py-3 bg-dark/80 backdrop-blur-md">
        <div class="flex gap-2.5 max-w-full">
          <div class="flex-1 relative">
            <input
              v-model="query"
              @keydown.enter="sendQuery"
              :disabled="loading"
              type="text"
              :placeholder="rounds.length ? 'Ask a follow-up or request a custom chart...' : 'Ask about your data...'"
              class="w-full bg-surface-card/60 border border-border/40 rounded-xl px-4 py-2.5 pr-16 text-sm text-text placeholder-muted/40 focus:outline-none focus:border-primary/40 focus:bg-surface-card transition disabled:opacity-40"
            />
            <div v-if="!loading && !query && !rounds.length" class="absolute right-2.5 top-1/2 -translate-y-1/2 flex items-center gap-1.5">
              <kbd class="text-[9px] text-muted/30 border border-border/30 rounded px-1 py-0.5 font-mono">Enter</kbd>
              <span class="text-[9px] text-muted/20">=</span>
              <span class="text-[9px] text-muted/30">full analysis</span>
            </div>
          </div>
          <button
            @click="sendQuery"
            :disabled="loading"
            class="w-10 h-10 bg-primary rounded-xl flex items-center justify-center hover:bg-primary/80 disabled:opacity-30 disabled:cursor-not-allowed transition-all active:scale-95 shadow-lg shadow-primary/20"
          >
            <svg v-if="!loading" class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
            </svg>
            <svg v-else class="w-4 h-4 text-white animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Fullscreen chart modal -->
    <div v-if="chartModal" class="fixed inset-0 z-50 flex items-center justify-center bg-dark/90 backdrop-blur-sm animate-fade-in" @click.self="chartModal = null">
      <div class="relative max-w-5xl max-h-[90vh] w-full mx-6">
        <button @click="chartModal = null" class="absolute -top-10 right-0 text-muted hover:text-white transition flex items-center gap-1.5 text-xs">
          <span>Close</span>
          <kbd class="text-[9px] border border-border/40 rounded px-1 py-0.5 font-mono">Esc</kbd>
        </button>
        <div class="rounded-2xl overflow-hidden border border-border/40 bg-surface-card shadow-2xl shadow-dark/80">
          <img :src="'data:image/png;base64,' + modalChart.image" class="w-full" alt="Chart" />
          <div class="px-4 py-2.5 border-t border-border/30 flex items-center justify-between">
            <span class="text-xs text-white font-medium">{{ modalChart.label || 'Visualization' }}</span>
            <button @click.stop="downloadModalChart" class="w-6 h-6 rounded-md border border-border/40 flex items-center justify-center text-muted hover:text-primary-light hover:border-primary/30 transition">
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, nextTick, onUnmounted, onMounted, watch } from 'vue'

const props = defineProps({
  fileInfo: { type: Object, required: true }
})

defineEmits(['reset'])

const query = ref('')
const rounds = reactive([])
const currentMessages = ref([])
const loading = ref(false)
const sidebarOpen = ref(true)
const chartModal = ref(null)
const showDataPreview = ref(false)
const dataPreviewRows = ref([])
const copiedRound = ref(null)
const sidebarScroll = ref(null)
const dashboardScroll = ref(null)
const analysisStartTime = ref(null)
const analysisTime = ref(null)
const timerTick = ref(0)
const timerInterval = ref(null)
let ws = null

const chartLabels = ['Distributions', 'Correlation Matrix', 'Categories']

const quickActions = [
  { label: 'Full analysis', query: 'Generate a complete analysis report', primary: true, icon: '<svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" /></svg>' },
  { label: 'Key patterns', query: 'What are the key patterns and correlations?', primary: false, icon: '<svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 18L9 11.25l4.306 4.307a11.95 11.95 0 015.814-5.519l2.74-1.22m0 0l-5.94-2.28m5.94 2.28l-2.28 5.941" /></svg>' },
  { label: 'Scatter plot', query: 'Create a scatter plot of the two most correlated numeric columns', primary: false, icon: '<svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75z" /></svg>' },
  { label: 'Outliers', query: 'Find outliers and anomalies in the data', primary: false, icon: '<svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126z" /></svg>' },
  { label: 'Data quality', query: 'Check data quality: missing values, duplicates, and data type issues', primary: false, icon: '<svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" /></svg>' }
]

const followUpActions = [
  { label: 'Scatter plot of top features', query: 'Create a scatter plot of the two most correlated numeric features colored by the first categorical column', icon: '<svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75z" /></svg>' },
  { label: 'Box plots comparison', query: 'Create box plots comparing all numeric columns grouped by the first categorical column', icon: '<svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M7.5 14.25v2.25m3-4.5v4.5m3-6.75v6.75m3-9v9M6 20.25h12A2.25 2.25 0 0020.25 18V6A2.25 2.25 0 0018 3.75H6A2.25 2.25 0 003.75 6v12A2.25 2.25 0 006 20.25z" /></svg>' },
  { label: 'Deep dive correlations', query: 'Show detailed correlation analysis between the top correlated features. Explain what each correlation means.', icon: '<svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13.19 8.688a4.5 4.5 0 011.242 7.244l-4.5 4.5a4.5 4.5 0 01-6.364-6.364l1.757-1.757m9.86-2.54a4.5 4.5 0 00-6.364-6.364L6.518 5.27a4.5 4.5 0 001.242 7.244" /></svg>' },
  { label: 'Recommendations', query: 'Based on the analysis, give me 5 actionable business recommendations with specific metrics.', icon: '<svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 18v-5.25m0 0a6.01 6.01 0 001.5-.189m-1.5.189a6.01 6.01 0 01-1.5-.189m3.75 7.478a12.06 12.06 0 01-4.5 0m3.75 2.383a14.406 14.406 0 01-3 0M14.25 18v-.192c0-.983.658-1.823 1.508-2.316a7.5 7.5 0 10-7.517 0c.85.493 1.509 1.333 1.509 2.316V18" /></svg>' }
]

const currentRound = computed(() => rounds.length ? rounds[rounds.length - 1] : null)
const currentRoundComplete = computed(() => currentRound.value && currentRound.value.answer)
const lastRoundComplete = computed(() => currentRoundComplete.value)

const currentActivity = computed(() =>
  currentMessages.value.filter(m => ['status', 'thought', 'code', 'output'].includes(m.type))
)

const analysisSteps = computed(() => {
  const thoughts = currentMessages.value.filter(m => m.type === 'thought').map(m => m.content)
  const hasPreview = thoughts.some(t => t.includes('data_preview'))
  const hasPythonRepl = thoughts.some(t => t.includes('python_repl'))
  const hasCharts = currentRound.value ? currentRound.value.charts.length > 0 : false
  const hasAnswer = currentRound.value ? !!currentRound.value.answer : false

  return [
    { label: 'EXPLORE', done: hasPreview, active: loading.value && !hasPreview && !hasPythonRepl },
    { label: 'ANALYZE', done: hasPythonRepl, active: loading.value && hasPreview && !hasPythonRepl },
    { label: 'VISUALIZE', done: hasCharts, active: loading.value && hasPythonRepl && !hasCharts && !hasAnswer },
    { label: 'REPORT', done: hasAnswer, active: loading.value && (hasPythonRepl || hasPreview) && !hasAnswer }
  ]
})

const modalChart = computed(() => {
  if (!chartModal.value) return null
  const round = rounds[chartModal.value.round]
  return round ? round.charts[chartModal.value.chart] : null
})

const formattedTime = computed(() => {
  timerTick.value
  const ms = loading.value ? (Date.now() - (analysisStartTime.value || Date.now())) : (analysisTime.value || 0)
  const secs = Math.floor(ms / 1000)
  const tenths = Math.floor((ms % 1000) / 100)
  return `${secs}.${tenths}s`
})

function scrollSidebar() {
  nextTick(() => { if (sidebarScroll.value) sidebarScroll.value.scrollTop = sidebarScroll.value.scrollHeight })
}

function scrollDashboard() {
  nextTick(() => {
    if (dashboardScroll.value) dashboardScroll.value.scrollTo({ top: dashboardScroll.value.scrollHeight, behavior: 'smooth' })
  })
}

watch(currentActivity, scrollSidebar, { deep: true })
watch(() => currentRound.value?.charts?.length, scrollDashboard)
watch(() => currentRound.value?.answer, scrollDashboard)

function connectWebSocket() {
  return new Promise((resolve, reject) => {
    if (ws && ws.readyState === WebSocket.OPEN) return resolve()
    ws = new WebSocket(`ws://localhost:8000/ws/analyze/${props.fileInfo.file_id}`)
    ws.onopen = () => resolve()
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      currentMessages.value.push(data)

      if (currentRound.value) {
        if (data.type === 'chart') {
          currentRound.value.charts.push({ image: data.image, label: data.label || null })
        } else if (data.type === 'answer') {
          currentRound.value.answer = data.content
          loading.value = false
          analysisTime.value = Date.now() - analysisStartTime.value
          clearInterval(timerInterval.value)
        } else if (data.type === 'error') {
          currentRound.value.errors.push(data.content)
          loading.value = false
          analysisTime.value = Date.now() - analysisStartTime.value
          clearInterval(timerInterval.value)
        }
      }
    }
    ws.onclose = () => {
      if (loading.value) {
        loading.value = false
        clearInterval(timerInterval.value)
        if (currentRound.value) currentRound.value.errors.push('Connection lost')
      }
    }
    ws.onerror = () => { loading.value = false; clearInterval(timerInterval.value); reject(new Error('WebSocket failed')) }
  })
}

function quickQuery(q) { query.value = q; sendQuery() }

async function sendQuery() {
  if (loading.value) return
  const q = query.value.trim() || 'Analyze this dataset thoroughly. Show key statistics, distributions, correlations, and generate visualizations for the most important findings.'

  rounds.push({ query: q, charts: [], answer: null, errors: [] })
  currentMessages.value = []
  loading.value = true
  query.value = ''
  analysisStartTime.value = Date.now()
  analysisTime.value = null
  timerInterval.value = setInterval(() => { timerTick.value++ }, 100)

  try {
    await connectWebSocket()
    ws.send(JSON.stringify({ query: q }))
  } catch (e) {
    loading.value = false
    clearInterval(timerInterval.value)
    if (currentRound.value) currentRound.value.errors.push('Failed to connect to server')
  }
}

function openChartModal(roundIdx, chartIdx) {
  chartModal.value = { round: roundIdx, chart: chartIdx }
}

function downloadModalChart() {
  if (!modalChart.value) return
  const link = document.createElement('a')
  link.download = `chart-${modalChart.value.label || 'visualization'}.png`
  link.href = 'data:image/png;base64,' + modalChart.value.image
  link.click()
}

function downloadRoundCharts(ri) {
  const round = rounds[ri]
  round.charts.forEach((chart, i) => {
    setTimeout(() => {
      const link = document.createElement('a')
      link.download = `chart-${i + 1}.png`
      link.href = 'data:image/png;base64,' + chart.image
      link.click()
    }, i * 200)
  })
}

function copyText(text) {
  navigator.clipboard.writeText(text)
  const ri = rounds.findIndex(r => r.answer === text)
  copiedRound.value = ri
  setTimeout(() => { copiedRound.value = null }, 2000)
}

function handleKeydown(e) {
  if (e.key === 'Escape' && chartModal.value) chartModal.value = null
}

async function fetchDataPreview() {
  try {
    const res = await fetch(`http://localhost:8000/preview/${props.fileInfo.file_id}`)
    if (res.ok) { const data = await res.json(); dataPreviewRows.value = data.rows }
  } catch (e) { dataPreviewRows.value = [] }
}

onMounted(() => { document.addEventListener('keydown', handleKeydown) })
onUnmounted(() => { if (ws) ws.close(); clearInterval(timerInterval.value); document.removeEventListener('keydown', handleKeydown) })
watch(showDataPreview, (val) => { if (val && dataPreviewRows.value.length === 0) fetchDataPreview() })

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
