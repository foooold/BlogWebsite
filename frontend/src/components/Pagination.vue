<template>
  <div class="pagination" v-if="totalPages > 1">
    <button :disabled="current === 1" @click="$emit('change', current - 1)">上一页</button>
    <template v-for="p in displayedPages" :key="p">
      <span v-if="p === '...'" class="ellipsis">...</span>
      <button
        v-else
        :class="{ active: p === current }"
        @click="$emit('change', p)"
      >{{ p }}</button>
    </template>
    <button :disabled="current === totalPages" @click="$emit('change', current + 1)">下一页</button>
    <span class="info">{{ current }} / {{ totalPages }} 页，共 {{ total }} 篇</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  current: { type: Number, required: true },
  total: { type: Number, required: true },
  perPage: { type: Number, default: 5 },
})

defineEmits(['change'])

const totalPages = computed(() => Math.ceil(props.total / props.perPage))

const displayedPages = computed(() => {
  const pages = []
  const total = totalPages.value
  const curr = props.current

  if (total <= 7) {
    for (let i = 1; i <= total; i++) pages.push(i)
    return pages
  }

  pages.push(1)
  if (curr > 3) pages.push('...')

  const start = Math.max(2, curr - 1)
  const end = Math.min(total - 1, curr + 1)
  for (let i = start; i <= end; i++) pages.push(i)

  if (curr < total - 2) pages.push('...')
  pages.push(total)

  return pages
})
</script>

<style scoped>
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  padding: 1.5rem 0;
  flex-wrap: wrap;
}
button {
  padding: 0.35rem 0.8rem;
  font-size: 0.85rem;
  color: #c9d1d9;
  background: #21262d;
  border: 1px solid #30363d;
  border-radius: 6px;
  cursor: pointer;
}
button:hover:not(:disabled) {
  background: #30363d;
  border-color: #8b949e;
}
button:disabled {
  opacity: 0.4;
  cursor: default;
}
button.active {
  background: #1f6feb;
  border-color: #1f6feb;
  color: #ffffff;
}
.ellipsis {
  color: #8b949e;
  padding: 0 0.25rem;
}
.info {
  font-size: 0.8rem;
  color: #8b949e;
  margin-left: 1rem;
}
</style>
