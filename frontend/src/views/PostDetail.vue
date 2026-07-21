<template>
  <div class="post-page" v-if="post">
    <div class="back-link">
      <router-link to="/blog">← 返回博客列表</router-link>
    </div>

    <article>
      <header class="post-header">
        <h1>{{ post.title }}</h1>
        <div class="post-meta">
          <time :datetime="post.date">{{ post.date }}</time>
          <span class="separator">·</span>
          <span>{{ readTime }}</span>
          <span class="separator">·</span>
          <span>{{ chineseCharCount }} 字</span>
        </div>
        <div v-if="post.excerpt" class="post-excerpt">{{ post.excerpt }}</div>
        <div class="post-tags">
          <TagBadge v-for="tag in post.tags" :key="tag" :name="tag" />
        </div>
      </header>

      <div class="post-content" v-html="renderedContent"></div>
    </article>

    <div class="post-footer">
      <router-link to="/blog" class="back-btn">← 返回博客列表</router-link>
    </div>
  </div>

  <div v-else-if="loading" class="not-found">
    <h2>加载中...</h2>
  </div>

  <div v-else class="not-found">
    <h2>文章未找到</h2>
    <router-link to="/blog">返回博客列表</router-link>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { getArticle } from '@/api'
import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js'
import 'highlight.js/styles/github-dark.css'

const md = new MarkdownIt({
  breaks: true,
  linkify: true,
  typographer: true,
  highlight(str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        const highlighted = hljs.highlight(str, { language: lang }).value
        return `<pre class="code-block hljs"><code class="language-${lang}">${highlighted}</code></pre>\n`
      } catch (e) {}
    }
    const highlighted = hljs.highlightAuto(str).value
    return `<pre class="code-block hljs"><code>${highlighted}</code></pre>\n`
  },
})

md.inline.ruler.disable('autolink')

md.renderer.rules.code_inline = (tokens, idx) => {
  const token = tokens[idx]
  return `<code class="inline-code">${md.utils.escapeHtml(token.content)}</code>`
}

import TagBadge from '@/components/TagBadge.vue'

const route = useRoute()
const post = ref(null)
const loading = ref(true)

async function fetchPost(slug) {
  loading.value = true
  try {
    post.value = await getArticle(slug)
  } catch (e) {
    post.value = null
  } finally {
    loading.value = false
  }
}

onMounted(() => fetchPost(route.params.slug))

watch(() => route.params.slug, (slug) => {
  if (slug) fetchPost(slug)
})

const readTime = computed(() => {
  if (!post.value) return ''
  const mins = Math.max(1, Math.ceil(post.value.content.length / 400))
  return `${mins} 分钟阅读`
})

const chineseCharCount = computed(() => {
  if (!post.value) return 0
  const chinese = (post.value.content.match(/[\u4e00-\u9fff]/g) || []).length
  return chinese
})

const renderedContent = computed(() => {
  return post.value ? md.render(post.value.content) : ''
})

watch(renderedContent, () => {
  nextTick(() => {
    addCopyButtons()
  })
})

function addCopyButtons() {
  // 复制按钮
  document.querySelectorAll('.code-block').forEach(block => {
    if (block.querySelector('.copy-btn')) return
    const btn = document.createElement('button')
    btn.className = 'copy-btn'
    btn.textContent = '复制'
    btn.onclick = async () => {
      const code = block.querySelector('code')?.textContent || ''
      await navigator.clipboard.writeText(code)
      btn.textContent = '已复制'
      setTimeout(() => { btn.textContent = '复制' }, 2000)
    }
    block.appendChild(btn)
  })

  // 触屏设备：复制按钮始终可见
  if (window.matchMedia('(hover: none)').matches) {
    document.querySelectorAll('.copy-btn').forEach(btn => {
      btn.classList.add('touch-visible')
    })
  }

  // 表格包裹 overflow-x: auto
  document.querySelectorAll('.post-content table').forEach(table => {
    if (table.parentElement?.classList.contains('table-wrapper')) return
    const wrapper = document.createElement('div')
    wrapper.className = 'table-wrapper'
    table.parentNode.insertBefore(wrapper, table)
    wrapper.appendChild(table)
  })
}
</script>

<style scoped>
.post-page {
  max-width: 780px;
  margin: 0 auto;
  padding: 0 1rem;
}
.back-link {
  padding: 1rem 0;
}
.back-link a {
  color: #60a5fa;
  text-decoration: none;
  font-size: 0.85rem;
}
.back-link a:hover {
  text-decoration: underline;
}
.post-header {
  border-bottom: 1px solid #30363d;
  padding-bottom: 1.5rem;
  margin-bottom: 2rem;
}
.post-header h1 {
  font-size: 1.6rem;
  font-weight: 600;
  color: #e6edf3;
  line-height: 1.4;
  margin-bottom: 0.6rem;
}
.post-meta {
  font-size: 0.82rem;
  color: #8b949e;
  margin-bottom: 0.75rem;
}
.separator {
  margin: 0 0.4rem;
}
.post-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.post-excerpt {
  font-size: 0.9rem;
  color: #8b949e;
  line-height: 1.6;
  padding: 0.6rem 0.9rem;
  margin-bottom: 0.75rem;
  background: #161b22;
  border-left: 3px solid #30363d;
  border-radius: 4px;
}
.post-content {
  font-size: 16px;
  line-height: 1.8;
  color: #c9d1d9;
}
.post-content :deep(h2) {
  font-size: 1.2rem;
  font-weight: 600;
  color: #e6edf3;
  margin: 2rem 0 0.75rem;
  padding-bottom: 0.4rem;
  border-bottom: 1px solid #21262d;
}
.post-content :deep(h3) {
  font-size: 1.05rem;
  font-weight: 600;
  color: #e6edf3;
  margin: 1.5rem 0 0.5rem;
}
.post-content :deep(p) {
  margin: 0.75rem 0;
}
.post-content :deep(ul) {
  margin: 0.75rem 0;
  padding-left: 1.5rem;
}
.post-content :deep(li) {
  margin: 0.3rem 0;
}
.post-content :deep(strong) {
  font-weight: 600;
  color: #e6edf3;
}
.post-content :deep(ol) {
  margin: 0.75rem 0;
  padding-left: 1.5rem;
}
.post-content :deep(blockquote) {
  margin: 1rem 0;
  padding: 0.5rem 1rem;
  color: #8b949e;
  border-left: 3px solid #30363d;
}
.post-content :deep(a) {
  color: #60a5fa;
  text-decoration: none;
}
.post-content :deep(a:hover) {
  text-decoration: underline;
}
.post-content :deep(img) {
  max-width: 100%;
}
.post-content :deep(hr) {
  height: 1px;
  margin: 2rem 0;
  background: #30363d;
  border: 0;
}
.post-content :deep(h4) {
  font-size: 1rem;
  font-weight: 600;
  color: #e6edf3;
  margin: 1.25rem 0 0.5rem;
}
.post-content :deep(h5),
.post-content :deep(h6) {
  font-size: 0.95rem;
  font-weight: 600;
  color: #e6edf3;
  margin: 1.25rem 0 0.5rem;
}
.post-content :deep(.inline-code) {
  padding: 0.15rem 0.4rem;
  font-size: 0.85em;
  background: rgba(110, 118, 129, 0.15);
  border-radius: 4px;
  font-family: 'Cascadia Code', 'Fira Code', 'Menlo', 'Monaco', 'Consolas', 'Courier New', monospace;
  color: #c9d1d9;
}
.post-content :deep(.code-block) {
  margin: 0.75rem 0;
  padding: 1rem 1.25rem;
  background: #0d1117;
  border: 1px solid #30363d;
  border-radius: 6px;
  overflow-x: auto;
  position: relative;
}
.post-content :deep(.code-block code) {
  font-family: 'Cascadia Code', 'Fira Code', 'Consolas', monospace;
  font-size: 14px;
  line-height: 1.6;
  color: #c9d1d9;
  white-space: pre;
}
.post-content :deep(.code-block) .copy-btn {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  padding: 0.15rem 0.5rem;
  font-size: 0.72rem;
  color: #8b949e;
  background: #21262d;
  border: 1px solid #30363d;
  border-radius: 4px;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.2s;
}
.post-content :deep(.code-block:hover) .copy-btn {
  opacity: 1;
}
.post-content :deep(.copy-btn):hover {
  color: #e6edf3;
  background: #30363d;
}
.post-content :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 0.75rem 0;
  font-size: 0.88rem;
}

.post-content :deep(.table-wrapper) {
  overflow-x: auto;
  margin: 0.75rem 0;
}

.post-content :deep(.table-wrapper table) {
  margin: 0;
  min-width: 500px;
}
.post-content :deep(th),
.post-content :deep(td) {
  padding: 0.5rem 0.75rem;
  border: 1px solid #30363d;
  text-align: left;
}
.post-content :deep(th) {
  background: #161b22;
  font-weight: 600;
}
.post-footer {
  border-top: 1px solid #30363d;
  padding: 2rem 0;
  text-align: center;
}
.back-btn {
  color: #60a5fa;
  text-decoration: none;
  font-size: 0.9rem;
}
.back-btn:hover {
  text-decoration: underline;
}
.not-found {
  text-align: center;
  padding: 4rem 1rem;
  color: #8b949e;
}
.not-found h2 {
  color: #e6edf3;
  margin-bottom: 1rem;
}
.not-found a {
  color: #60a5fa;
}

/* 触屏设备：复制按钮始终可见 */
.post-content :deep(.copy-btn).touch-visible {
  opacity: 1;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .post-header h1 {
    font-size: 1.3rem;
  }

  .post-header {
    padding-bottom: 1rem;
    margin-bottom: 1.25rem;
  }

  .post-content {
    font-size: 15px;
    line-height: 1.75;
  }

  .post-content :deep(.code-block) {
    padding: 0.75rem;
    font-size: 13px;
  }

  .post-content :deep(.code-block code) {
    font-size: 13px;
  }

  .post-content :deep(h2) {
    font-size: 1.1rem;
    margin: 1.5rem 0 0.5rem;
  }

  .post-content :deep(h3) {
    font-size: 1rem;
  }

  .post-content :deep(.copy-btn) {
    opacity: 1;
  }

  .post-footer {
    padding: 1.5rem 0;
  }
}
</style>
