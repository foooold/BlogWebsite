import { computed, nextTick, ref } from 'vue'

const STORAGE_KEY = 'frank-blog-theme'
const theme = ref(document.documentElement.dataset.theme === 'light' ? 'light' : 'dark')
const isTransitioning = ref(false)

function applyTheme(nextTheme) {
  theme.value = nextTheme
  document.documentElement.dataset.theme = nextTheme
  document.documentElement.style.colorScheme = nextTheme
  localStorage.setItem(STORAGE_KEY, nextTheme)
}

export function useTheme() {
  const isDark = computed(() => theme.value === 'dark')

  async function toggleTheme(origin) {
    if (isTransitioning.value) return

    const nextTheme = isDark.value ? 'light' : 'dark'
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches

    if (!document.startViewTransition || reduceMotion || !origin || document.visibilityState !== 'visible') {
      applyTheme(nextTheme)
      return
    }

    const originX = Number(origin.x)
    const originY = Number(origin.y)
    if (!Number.isFinite(originX) || !Number.isFinite(originY)) {
      applyTheme(nextTheme)
      return
    }

    const x = Math.min(Math.max(originX, 0), window.innerWidth)
    const y = Math.min(Math.max(originY, 0), window.innerHeight)
    const radius = Math.hypot(
      Math.max(x, window.innerWidth - x),
      Math.max(y, window.innerHeight - y),
    )
    const root = document.documentElement

    isTransitioning.value = true
    try {
      root.classList.add('theme-transition')
      const transition = document.startViewTransition(async () => {
        applyTheme(nextTheme)
        await nextTick()
      })

      try {
        await transition.ready
      } catch (error) {
        console.warn('[theme] View transition was skipped before animation.', error)
        if (theme.value !== nextTheme) applyTheme(nextTheme)
        await transition.finished
        return
      }

      const reveal = root.animate(
        {
          clipPath: [
            `circle(0 at ${x}px ${y}px)`,
            `circle(${radius}px at ${x}px ${y}px)`,
          ],
        },
        {
          duration: 550,
          easing: 'cubic-bezier(0.4, 0, 0.2, 1)',
          fill: 'both',
          pseudoElement: '::view-transition-new(root)',
        },
      )

      await Promise.all([reveal.finished, transition.finished])
    } catch (error) {
      console.warn('[theme] Theme transition failed.', error)
      if (theme.value !== nextTheme) applyTheme(nextTheme)
    } finally {
      root.classList.remove('theme-transition')
      isTransitioning.value = false
    }
  }

  return { theme, isDark, isTransitioning, toggleTheme }
}
