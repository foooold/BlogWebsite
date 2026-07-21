<template>
  <div class="archive-page">
    <PageHeader title="归档" :description="`${allPosts.length} 篇文章`" />

    <div class="archive-list">
      <section v-for="group in archive" :key="group.key" class="archive-group">
        <h2 class="group-title">
          {{ group.year }} 年 {{ group.month }} 月
          <span class="group-count">{{ group.posts.length }} 篇</span>
        </h2>
        <div class="group-posts">
          <div
            v-for="post in group.posts"
            :key="post.id"
            class="archive-item"
          >
            <time class="item-date">{{ post.date }}</time>
            <router-link :to="`/blog/${post.slug}`" class="item-title">
              {{ post.title }}
            </router-link>
            <span class="item-tags">
              <TagBadge v-for="tag in post.tags" :key="tag" :name="tag" />
            </span>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getArticles } from '@/api'
import PageHeader from '@/components/PageHeader.vue'
import TagBadge from '@/components/TagBadge.vue'

const allPosts = ref([])

onMounted(async () => {
  try {
    allPosts.value = await getArticles()
  } catch (e) {
    console.error('Failed to load articles:', e)
  }
})

function getArchive() {
  const archive = {}
  for (const post of allPosts.value) {
    const [year, month] = post.date.split('-')
    const key = `${year}-${month}`
    if (!archive[key]) {
      archive[key] = { year, month, posts: [] }
    }
    archive[key].posts.push(post)
  }
  return Object.values(archive).sort((a, b) => {
    if (a.year !== b.year) return b.year - a.year
    return b.month - a.month
  })
}

const archive = computed(() => getArchive())
</script>

<style scoped>
.archive-page {
  max-width: 860px;
  margin: 0 auto;
  padding: 0 1rem;
}
.archive-group {
  margin-bottom: 2rem;
}
.group-title {
  font-size: 1.05rem;
  font-weight: 600;
  color: #e6edf3;
  margin-bottom: 0.75rem;
  padding-bottom: 0.4rem;
  border-bottom: 1px solid #21262d;
}
.group-count {
  font-size: 0.8rem;
  font-weight: 400;
  color: #8b949e;
  margin-left: 0.5rem;
}
.archive-item {
  display: flex;
  align-items: center;
  padding: 0.6rem 0.75rem;
  border: 1px solid #21262d;
  border-radius: 6px;
  margin-bottom: 0.4rem;
  gap: 0.75rem;
  flex-wrap: wrap;
}
.archive-item:hover {
  background: #161b22;
  border-color: #30363d;
}
.item-date {
  font-size: 0.8rem;
  color: #8b949e;
  white-space: nowrap;
  font-family: 'Cascadia Code', 'Fira Code', 'Consolas', monospace;
}
.item-title {
  font-size: 0.9rem;
  color: #60a5fa;
  text-decoration: none;
  flex: 1;
  min-width: 200px;
}
.item-title:hover {
  text-decoration: underline;
}
.item-tags {
  display: flex;
  gap: 0.4rem;
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .item-title {
    min-width: 0;
  }
}
</style>
