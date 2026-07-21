<template>
  <div class="page-header">
    <h1>{{ title }}</h1>
    <p v-if="description" class="desc">{{ description }}</p>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  description: { type: String, default: '' },
})
</script>

<style scoped>
.page-header {
  padding: 2rem 0 1.5rem;
  border-bottom: 1px solid #30363d;
  margin-bottom: 1.5rem;
}
h1 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #e6edf3;
}
.desc {
  margin-top: 0.5rem;
  color: #8b949e;
  font-size: 0.9rem;
}

/* 移动端：减小 padding */
@media (max-width: 768px) {
  .page-header {
    padding: 1.25rem 0 1rem;
    margin-bottom: 1rem;
  }

  h1 {
    font-size: 1.3rem;
  }
}
</style>
