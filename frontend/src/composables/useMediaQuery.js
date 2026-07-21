import { ref, onMounted, onBeforeUnmount } from 'vue'

export function useMediaQuery(query = '(max-width: 768px)') {
  const matches = ref(false)
  const update = (e) => { matches.value = e.matches }

  onMounted(() => {
    const mql = window.matchMedia(query)
    matches.value = mql.matches
    mql.addEventListener('change', update)
    onBeforeUnmount(() => mql.removeEventListener('change', update))
  })

  return matches
}
