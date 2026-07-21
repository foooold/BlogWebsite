import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  const message = ref('')
  const loading = ref(false)

  async function fetchHello() {
    loading.value = true
    try {
      const { getHello } = await import('@/api')
      const data = await getHello()
      message.value = data.message
    } finally {
      loading.value = false
    }
  }

  return { message, loading, fetchHello }
})
