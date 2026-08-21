<template>
  <article :class="['blog-card', { pinned: post.is_pinned }]">
    <span v-if="post.is_pinned" class="hole-punch"></span>
    <div class="card-body">
      <h2 class="title">
        <router-link :to="`/blog/${post.slug}`">{{ post.title }}</router-link>
      </h2>
      <div class="meta">
        <template v-if="post.author_name">
          <span class="author">{{ post.author_name }}</span>
          <span class="separator">·</span>
        </template>
        <time :datetime="post.date">{{ post.date }}</time>
        <span class="separator">·</span>
        <span class="read-time">{{ readTime }}</span>
      </div>
      <p class="excerpt" v-html="renderedExcerpt"></p>
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
import MarkdownIt from 'markdown-it'
import TagBadge from './TagBadge.vue'

const md = new MarkdownIt({
  html: true,
  breaks: true,
  linkify: true,
})

md.renderer.rules.code_inline = (tokens, idx) => {
  const token = tokens[idx]
  return `<code class="inline-code">${md.utils.escapeHtml(token.content)}</code>`
}

const props = defineProps({
  post: { type: Object, required: true },
})

const renderedExcerpt = computed(() => {
  return props.post?.excerpt ? md.render(props.post.excerpt) : ''
})

const readTime = computed(() => {
  const chars = props.post.word_count || 0
  const mins = Math.max(1, Math.ceil(chars / 400))
  return `${mins} 分钟阅读`
})
</script>

<style scoped>
.blog-card {
  border: 1px solid var(--border-default);
  border-radius: 6px;
  background: var(--bg-default);
  margin-bottom: 1rem;
  position: relative;
}
.blog-card.pinned {
  border-left: 3px solid var(--accent-emphasis);
}
.hole-punch {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 18px;
  height: 18px;
  background: var(--bg-canvas);
  border: 1px solid var(--border-default);
  border-radius: 50%;
  z-index: 1;
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
  color: var(--accent);
  text-decoration: none;
}
.title a:hover {
  text-decoration: underline;
}
.meta {
  font-size: 0.8rem;
  color: var(--fg-muted);
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0 0.4rem;
}
.read-time {
  color: var(--fg-muted);
}
.excerpt {
  font-size: 0.9rem;
  color: var(--fg-default);
  line-height: 1.6;
  margin-bottom: 0.75rem;
}
.excerpt :deep(.inline-code) {
  padding: 0.15rem 0.4rem;
  font-size: 0.85em;
  background: var(--inline-code-bg);
  border-radius: 4px;
  font-family: 'Cascadia Code', 'Fira Code', 'Menlo', 'Monaco', 'Consolas', 'Courier New', monospace;
  color: var(--fg-default);
}
.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

@media (max-width: 768px) {
  .card-body {
    padding: 1rem;
  }
}
</style>
