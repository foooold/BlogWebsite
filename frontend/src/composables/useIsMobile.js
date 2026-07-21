import { ref, onMounted, onBeforeUnmount } from 'vue'

const BREAKPOINT = 768

const isMobile = ref(false)

function check() {
  isMobile.value = window.innerWidth < BREAKPOINT
}

let listeners = 0

export function useIsMobile() {
  onMounted(() => {
    if (listeners === 0) {
      check()
      window.addEventListener('resize', check)
    }
    listeners++
  })

  onBeforeUnmount(() => {
    listeners--
    if (listeners === 0) {
      window.removeEventListener('resize', check)
    }
  })

  return { isMobile }
}
