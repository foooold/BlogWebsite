<template>
  <div class="tags-page">
    <PageHeader title="标签" :description="`${allTags.length} 个标签`" />

    <div class="tags-cloud">
      <button
        v-for="tag in allTags"
        :key="tag.name"
        :class="['tag-chip', { active: activeTag === tag.name }]"
        @click="toggleTag(tag.name)"
      >
        {{ tag.name }}
        <span class="chip-count">{{ tag.count }}</span>
      </button>
    </div>

    <div v-if="activeTag" class="tagged-posts">
      <div class="tagged-header">
        <h2>
          标签「<em>{{ activeTag }}</em>」下的文章（{{ taggedPosts.length }} 篇）
        </h2>
        <button class="clear-btn" @click="activeTag = null">清除筛选</button>
      </div>
      <BlogCard v-for="post in taggedPosts" :key="post.id" :post="post" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getArticles, getTags } from '@/api'
import PageHeader from '@/components/PageHeader.vue'
import BlogCard from '@/components/BlogCard.vue'

const allTags = ref([])
const allPosts = ref([])
const activeTag = ref(null)

onMounted(async () => {
  try {
    const [articles, tags] = await Promise.all([getArticles(), getTags()])
    allPosts.value = articles
    allTags.value = tags
  } catch (e) {
    console.error('Failed to load data:', e)
  }
})

const taggedPosts = computed(() => {
  if (!activeTag.value) return []
  return allPosts.value.filter((p) => p.tags.includes(activeTag.value))
})

function toggleTag(name) {
  activeTag.value = activeTag.value === name ? null : name
}
</script>

<style scoped>
.tags-page {
  max-width: 860px;
  margin: 0 auto;
  padding: 0 1rem;
}
.tags-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 2rem;
}
.tag-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.4rem 0.85rem;
  font-size: 0.85rem;
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
</style>
