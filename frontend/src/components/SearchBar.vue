<template>
  <div class="search-wrapper" ref="wrapperRef">
    <div class="search-input-group" :class="{ focused: isFocused }">
      <svg class="search-icon" width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
        <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"/>
      </svg>
      <input
        ref="inputRef"
        v-model="query"
        type="text"
        class="search-input"
        placeholder="搜索文章或标签…"
        @focus="onFocus"
        @blur="onBlur"
        @keydown="onKeydown"
      />
      <span v-if="!isFocused && !query" class="search-shortcut">/</span>
    </div>

    <div v-if="showDropdown" class="search-dropdown">
      <!-- loading -->
      <div v-if="loading" class="search-status">搜索中…</div>

      <!-- no results -->
      <template v-else-if="!hasResults">
        <div class="search-status">未找到相关文章或标签</div>
      </template>

      <!-- results -->
      <template v-else>
        <!-- tag results -->
        <div v-if="results.tags.length" class="search-section">
          <div class="search-section-title">标签</div>
          <div
            v-for="(tag, idx) in results.tags"
            :key="'tag-' + tag.slug"
            class="search-result-item"
            :class="{ highlighted: highlightedIdx === idx }"
            @mousedown.prevent="goToTag(tag)"
            @mouseenter="highlightedIdx = idx"
          >
            <span class="result-tag-badge" v-html="highlightText('# ' + tag.name, query)"></span>
            <span class="result-tag-count">{{ tag.count }} 篇</span>
          </div>
        </div>

        <!-- article results -->
        <div v-if="results.articles.length" class="search-section">
          <div class="search-section-title">文章</div>
          <div
            v-for="(article, idx) in results.articles"
            :key="'article-' + article.slug"
            class="search-result-item"
            :class="{ highlighted: highlightedIdx === (idx + articleOffset) }"
            @mousedown.prevent="goToArticle(article)"
            @mouseenter="highlightedIdx = idx + articleOffset"
          >
            <div class="result-title" v-html="highlightText(article.title, query)"></div>
            <div v-if="article.snippet" class="result-excerpt" v-html="highlightText(article.snippet, query)"></div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { searchArticles } from '@/api'

const router = useRouter()
const query = ref('')
const results = ref({ articles: [], tags: [] })
const loading = ref(false)
const isFocused = ref(false)
const highlightedIdx = ref(-1)
const inputRef = ref(null)
const wrapperRef = ref(null)

let debounceTimer = null

const articleOffset = computed(() => results.value.tags.length)

const totalResults = computed(() => results.value.tags.length + results.value.articles.length)

const hasResults = computed(() => totalResults.value > 0)

const showDropdown = computed(() => isFocused.value && query.value.trim().length > 0)

function onFocus() {
  isFocused.value = true
  if (query.value.trim()) {
    doSearch()
  }
}

function onBlur() {
  // delay to allow mousedown on dropdown items
  setTimeout(() => {
    isFocused.value = false
    highlightedIdx.value = -1
  }, 150)
}

function onKeydown(e) {
  if (!showDropdown.value) return

  if (e.key === 'ArrowDown') {
    e.preventDefault()
    highlightedIdx.value = (highlightedIdx.value + 1) % totalResults.value
  } else if (e.key === 'ArrowUp') {
    e.preventDefault()
    highlightedIdx.value = (highlightedIdx.value - 1 + totalResults.value) % totalResults.value
  } else if (e.key === 'Enter') {
    e.preventDefault()
    selectHighlighted()
  } else if (e.key === 'Escape') {
    e.preventDefault()
    inputRef.value?.blur()
    isFocused.value = false
    highlightedIdx.value = -1
  }
}

function selectHighlighted() {
  const idx = highlightedIdx.value
  if (idx < 0 || idx >= totalResults.value) return

  if (idx < results.value.tags.length) {
    goToTag(results.value.tags[idx])
  } else {
    goToArticle(results.value.articles[idx - results.value.tags.length])
  }
}

function goToArticle(article) {
  query.value = ''
  results.value = { articles: [], tags: [] }
  router.push('/blog/' + article.slug)
}

function goToTag(tag) {
  query.value = ''
  results.value = { articles: [], tags: [] }
  router.push('/blog?tag=' + encodeURIComponent(tag.name))
}

function doSearch() {
  const q = query.value.trim()
  if (!q) {
    results.value = { articles: [], tags: [] }
    return
  }
  loading.value = true
  highlightedIdx.value = -1
  searchArticles(q).then((data) => {
    results.value = data
  }).catch(() => {
    results.value = { articles: [], tags: [] }
  }).finally(() => {
    loading.value = false
  })
}

watch(query, () => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    doSearch()
  }, 300)
})

function highlightText(text, q) {
  if (!q || !text) return text
  const escaped = q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  const re = new RegExp(`(${escaped})`, 'gi')
  return text.replace(re, '<mark class="search-highlight">$1</mark>')
}

function onGlobalKeydown(e) {
  // ignore if already in an input/textarea/contenteditable
  const tag = e.target.tagName
  if (tag === 'INPUT' || tag === 'TEXTAREA' || e.target.isContentEditable) return
  // ignore if modifier keys are pressed
  if (e.ctrlKey || e.metaKey || e.altKey) return

  if (e.key === '/') {
    e.preventDefault()
    inputRef.value?.focus()
  }
}

onMounted(() => {
  document.addEventListener('keydown', onGlobalKeydown)
})

onBeforeUnmount(() => {
  document.removeEventListener('keydown', onGlobalKeydown)
  clearTimeout(debounceTimer)
})
</script>

<style scoped>
.search-wrapper {
  position: relative;
}

.search-input-group {
  display: flex;
  align-items: center;
  background: #0d1117;
  border: 1px solid #30363d;
  border-radius: 6px;
  padding: 0 0.5rem;
  height: 30px;
  width: 220px;
  transition: width 0.2s ease, border-color 0.2s ease;
}

.search-input-group.focused {
  border-color: #58a6ff;
  width: 320px;
}

.search-icon {
  color: #484f58;
  flex-shrink: 0;
  margin-right: 0.35rem;
}

.search-input-group.focused .search-icon {
  color: #8b949e;
}

.search-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  color: #c9d1d9;
  font-size: 0.82rem;
  font-family: inherit;
  min-width: 0;
}

.search-input::placeholder {
  color: #484f58;
}

.search-shortcut {
  flex-shrink: 0;
  font-size: 0.7rem;
  color: #484f58;
  border: 1px solid #30363d;
  border-radius: 3px;
  padding: 0 4px;
  line-height: 1.2;
  font-family: inherit;
}

.search-dropdown {
  position: absolute;
  top: calc(100% + 4px);
  right: 0;
  width: 380px;
  max-width: calc(100vw - 2rem);
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 6px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
  max-height: 420px;
  overflow-y: auto;
  z-index: 100;
}

.search-section {
  padding: 0.35rem 0;
}

.search-section + .search-section {
  border-top: 1px solid #21262d;
}

.search-section-title {
  padding: 0.35rem 0.75rem;
  font-size: 0.7rem;
  font-weight: 600;
  color: #8b949e;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.search-result-item {
  padding: 0.45rem 0.75rem;
  cursor: pointer;
}

.search-result-item.highlighted {
  background: #1f6feb;
}

.search-result-item.highlighted .result-title,
.search-result-item.highlighted .result-excerpt,
.search-result-item.highlighted .result-tag-badge,
.search-result-item.highlighted .result-tag-count {
  color: #fff;
}

.result-title {
  font-size: 0.85rem;
  color: #c9d1d9;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.result-excerpt {
  font-size: 0.75rem;
  color: #8b949e;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-top: 1px;
}

.result-tag-badge {
  font-size: 0.82rem;
  color: #58a6ff;
  font-weight: 500;
}

.result-tag-count {
  font-size: 0.72rem;
  color: #8b949e;
  margin-left: 0.5rem;
}

.search-status {
  padding: 0.75rem;
  text-align: center;
  font-size: 0.82rem;
  color: #8b949e;
}

:deep(.search-highlight) {
  background: rgba(88, 166, 255, 0.22);
  color: #79c0ff;
  border-radius: 2px;
  padding: 0 1px;
}
</style>
