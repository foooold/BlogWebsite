<template>
  <span class="tag-badge">{{ name }}</span>
</template>

<script setup>
defineProps({
  name: { type: String, required: true },
})
</script>

<style scoped>
.tag-badge {
  display: inline-block;
  padding: 2px 10px;
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--tag-fg);
  background: var(--tag-bg);
  border: 1px solid var(--tag-border);
  border-radius: 12px;
  line-height: 1.6;
}
.tag-badge:hover {
  color: var(--tag-hover-fg);
  background: var(--tag-hover-bg);
  border-color: var(--tag-hover-border);
}
</style>
