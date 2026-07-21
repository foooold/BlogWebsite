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
  color: #60a5fa;
  background: rgba(96, 165, 250, 0.1);
  border: 1px solid rgba(96, 165, 250, 0.2);
  border-radius: 12px;
  line-height: 1.6;
}
.tag-badge:hover {
  background: rgba(96, 165, 250, 0.15);
  border-color: rgba(96, 165, 250, 0.35);
}
</style>
