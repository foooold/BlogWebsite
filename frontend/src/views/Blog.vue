<template>
  <div class="blog-page">
    <PageHeader title="博客" :description="`共 ${allPosts.length} 篇文章`" />

    <div class="tags-cloud">
      <button
        v-for="tag in allTags"
        :key="tag.name"
        :class="['tag-chip', { active: tagFilters.includes(tag.name) }]"
        @click="toggleTag(tag.name)"
      >
        {{ tag.name }}
        <span class="chip-count">{{ tag.count }}</span>
      </button>
    </div>

    <div v-if="tagFilters.length > 0" class="tagged-header">
      <h2>标签「<em>{{ tagFilters.join(' + ') }}</em>」下的文章（{{ filteredPosts.length }} 篇）</h2>
      <button class="clear-btn" @click="tagFilters = []">清除筛选</button>
    </div>

    <div v-if="filteredPosts.length === 0" class="empty">
      没有找到匹配的文章
    </div>

    <BlogCard v-for="post in pagedPosts" :key="post.id" :post="post" />

    <Pagination
      :current="currentPage"
      :total="filteredPosts.length"
      :per-page="perPage"
      @change="currentPage = $event"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getArticles, getTags } from '@/api'

const route = useRoute()
import PageHeader from '@/components/PageHeader.vue'
import BlogCard from '@/components/BlogCard.vue'
import Pagination from '@/components/Pagination.vue'

const allPosts = ref([])
const allTags = ref([])
const perPage = 5

const currentPage = ref(1)
const tagFilters = ref([])

onMounted(async () => {
  try {
    const [articles, tags] = await Promise.all([getArticles(), getTags()])
    allPosts.value = articles
    allTags.value = tags
  } catch (e) {
    console.error('Failed to load data:', e)
  }
  const tagFromQuery = route.query.tag
  if (tagFromQuery) {
    tagFilters.value = [tagFromQuery]
  }
})

watch(() => route.query.tag, (newTag) => {
  tagFilters.value = newTag ? [newTag] : []
  currentPage.value = 1
})

const filteredPosts = computed(() => {
  let result = allPosts.value
  if (tagFilters.value.length > 0) {
    result = result.filter((p) => tagFilters.value.every((t) => p.tags.includes(t)))
  }
  return result
})

function toggleTag(name) {
  const idx = tagFilters.value.indexOf(name)
  if (idx === -1) {
    tagFilters.value.push(name)
  } else {
    tagFilters.value.splice(idx, 1)
  }
}

const pagedPosts = computed(() => {
  const start = (currentPage.value - 1) * perPage
  return filteredPosts.value.slice(start, start + perPage)
})
</script>

<style scoped>
.blog-page {
  max-width: 860px;
  margin: 0 auto;
  padding: 0 1rem;
}
.empty {
  text-align: center;
  color: #8b949e;
  padding: 3rem 0;
  font-size: 0.95rem;
}
.tags-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}
.tagged-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.6rem;
  border-bottom: 1px solid #21262d;
}
.tagged-header h2 {
  font-size: 0.95rem;
  font-weight: 400;
  color: #8b949e;
}
.tagged-header em {
  font-style: normal;
  color: #60a5fa;
  font-weight: 600;
}
.clear-btn {
  padding: 0.25rem 0.6rem;
  font-size: 0.8rem;
  color: #c9d1d9;
  background: #21262d;
  border: 1px solid #30363d;
  border-radius: 6px;
  cursor: pointer;
}
.clear-btn:hover {
  background: #30363d;
}
.tag-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.4rem 0.65rem;
  font-size: 0.8rem;
  color: #c9d1d9;
  background: #21262d;
  border: 1px solid #30363d;
  border-radius: 6px;
  cursor: pointer;
}
.tag-chip:hover {
  background: #30363d;
  border-color: #8b949e;
}
.tag-chip.active {
  background: rgba(31, 111, 235, 0.15);
  border-color: #1f6feb;
  color: #60a5fa;
}
.chip-count {
  font-size: 0.72rem;
  color: #8b949e;
  background: rgba(110, 118, 129, 0.15);
  padding: 1px 6px;
  border-radius: 10px;
}
.tag-chip.active .chip-count {
  background: rgba(31, 111, 235, 0.2);
  color: #60a5fa;
}
</style>
