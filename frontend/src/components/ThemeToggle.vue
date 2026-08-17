<template>
  <button
    class="theme-toggle"
    :class="{ 'is-dark': isDark }"
    type="button"
    role="switch"
    :aria-checked="isDark"
    :aria-busy="isTransitioning"
    :disabled="isTransitioning"
    :aria-label="isDark ? '切换到浅色模式' : '切换到深色模式'"
    :title="isDark ? '切换到浅色模式' : '切换到深色模式'"
    @click="handleToggle"
  >
    <span class="theme-toggle__thumb">
      <svg v-if="isDark" aria-hidden="true" viewBox="0 0 24 24" fill="none">
        <path d="M3.32031 11.6835C3.32031 16.6541 7.34975 20.6835 12.3203 20.6835C16.1075 20.6835 19.3483 18.3443 20.6768 15.032C19.6402 15.4486 18.5059 15.6834 17.3203 15.6834C12.3497 15.6834 8.32031 11.654 8.32031 6.68342C8.32031 5.50338 8.55165 4.36259 8.96453 3.32996C5.65605 4.66028 3.32031 7.89912 3.32031 11.6835Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      <svg v-else aria-hidden="true" viewBox="0 0 24 24" fill="none">
        <path d="M12 3V4M12 20V21M4 12H3M6.31412 6.31412L5.5 5.5M17.6859 6.31412L18.5 5.5M6.31412 17.69L5.5 18.5001M17.6859 17.69L18.5 18.5001M21 12H20M16 12C16 14.2091 14.2091 16 12 16C9.79086 16 8 14.2091 8 12C8 9.79086 9.79086 8 12 8C14.2091 8 16 9.79086 16 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </span>
  </button>
</template>

<script setup>
import { useTheme } from '@/composables/useTheme'

const { isDark, isTransitioning, toggleTheme } = useTheme()

function handleToggle(event) {
  const rect = event.currentTarget.getBoundingClientRect()
  toggleTheme({
    x: rect.left + rect.width / 2,
    y: rect.top + rect.height / 2,
  })
}
</script>

<style scoped>
.theme-toggle {
  display: inline-flex;
  align-items: center;
  width: 46px;
  height: 26px;
  padding: 3px;
  background: var(--bg-muted);
  border: 1px solid var(--border-default);
  border-radius: 999px;
  cursor: pointer;
  transition: background-color 0.2s ease, border-color 0.2s ease;
}
.theme-toggle:hover {
  background: var(--control-hover-bg);
  border-color: var(--control-hover-accent-border);
}
.theme-toggle:focus-visible {
  outline: 2px solid var(--accent-focus);
  outline-offset: 2px;
}
.theme-toggle:disabled { cursor: wait; }
.theme-toggle.is-dark { background: var(--bg-muted); }
.theme-toggle__thumb {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: var(--bg-default);
  color: var(--fg-default);
  box-shadow: 0 1px 2px var(--shadow);
  transition: transform 0.2s ease;
}
.theme-toggle.is-dark .theme-toggle__thumb { transform: translateX(20px); }
.theme-toggle svg { width: 12px; height: 12px; }
</style>
