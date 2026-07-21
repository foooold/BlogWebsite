<template>
  <article class="blog-card">
    <div class="card-body">
      <h2 class="title">
        <router-link :to="`/blog/${post.slug}`">{{ post.title }}</router-link>
      </h2>
      <div class="meta">
        <time :datetime="post.date">{{ post.date }}</time>
        <span class="separator">·</span>
        <span class="read-time">{{ readTime }}</span>
      </div>
      <p class="excerpt">{{ post.excerpt }}</p>
      <div class="tags">
        <TagBadge
          v-for="tag in post.tags"
          :key="tag"
          :name="tag"
        />
      </div>
    </div>
  </article>
</template>

<script setup>
import { computed } from 'vue'
import TagBadge from './TagBadge.vue'

const props = defineProps({
  post: { type: Object, required: true },
})

const readTime = computed(() => {
  const chars = props.post.word_count || 0
  const mins = Math.max(1, Math.ceil(chars / 400))
  return `${mins} 分钟阅读`
})
</script>

<style scoped>
.blog-card {
  border: 1px solid #30363d;
  border-radius: 6px;
  background: #161b22;
  margin-bottom: 1rem;
}
.card-body {
  padding: 1.25rem 1.5rem;
}
.title {
  font-size: 1.15rem;
  font-weight: 600;
  margin-bottom: 0.4rem;
  line-height: 1.4;
}
.title a {
  color: #60a5fa;
  text-decoration: none;
}
.title a:hover {
  text-decoration: underline;
}
.meta {
  font-size: 0.8rem;
  color: #8b949e;
  margin-bottom: 0.75rem;
}
.separator {
  margin: 0 0.4rem;
}
.read-time {
  color: #8b949e;
}
.excerpt {
  font-size: 0.9rem;
  color: #c9d1d9;
  line-height: 1.6;
  margin-bottom: 0.75rem;
}
.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}
</style>
