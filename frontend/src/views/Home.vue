<template>
  <div class="home-page">
    <section class="hero">
      <div class="hero-avatar">
        <svg width="80" height="80" viewBox="0 0 80 80" fill="none" class="avatar-fallback">
          <circle cx="40" cy="40" r="40" fill="#30363d"/>
          <circle cx="40" cy="32" r="14" fill="#8b949e"/>
          <ellipse cx="40" cy="66" rx="24" ry="12" fill="#8b949e"/>
        </svg>
        <img v-show="!showFallback" :src="avatarUrl" alt="Frank Du" class="avatar-img" @error="onAvatarError" />
      </div>
      <h1 class="hero-name">Frank Du</h1>
      <p class="hero-bio">欢迎来到我的个人博客！</p>
      <div class="hero-stats">
        <div class="stat-item">
          <span class="stat-num">{{ stats.posts }}</span>
          <span class="stat-label">文章</span>
        </div>
        <div class="stat-item">
          <span class="stat-num">{{ stats.tags }}</span>
          <span class="stat-label">标签</span>
        </div>
        <div class="stat-item">
          <span class="stat-num">{{ stats.words }}</span>
          <span class="stat-label">字数</span>
        </div>
      </div>
      <div class="hero-links">
        <a href="https://github.com/foooold" target="_blank" class="hero-link">
          <svg width="18" height="18" viewBox="0 0 16 16" fill="currentColor"><path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
          GitHub
        </a>
        <span class="hero-link">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
          <polyline points="22,6 12,13 2,6"/>
          </svg>
          1474036970@qq.com
        </span>
      </div>
    </section>

    <section class="recent-posts">
      <div class="section-header">
        <h2>最新文章</h2>
        <router-link to="/blog" class="view-all">查看全部 →</router-link>
      </div>
      <div class="post-grid">
        <BlogCard v-for="post in recentPosts" :key="post.id" :post="post" />
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getArticles, getTags } from '@/api'
import BlogCard from '@/components/BlogCard.vue'

const avatarUrl = '/static/avatar.png'
const allPosts = ref([])
const allTags = ref([])

onMounted(async () => {
  try {
    const [articles, tags] = await Promise.all([getArticles(), getTags()])
    allPosts.value = articles
    allTags.value = tags
  } catch (e) {
    console.error('Failed to load data:', e)
  }
})

const recentPosts = computed(() => allPosts.value.slice(0, 5))

const showFallback = ref(false)

function onAvatarError() {
  showFallback.value = true
}

const stats = computed(() => {
  const totalChars = allPosts.value.reduce((sum, p) => sum + (p.word_count || 0), 0)
  return {
    posts: allPosts.value.length,
    tags: allTags.value.length,
    words: `${Math.floor(totalChars / 1000)}k`,
  }
})
</script>

<style scoped>
.home-page {
  max-width: 860px;
  margin: 0 auto;
  padding: 0 1rem;
}
.hero {
  text-align: center;
  padding: 2.5rem 1rem 2rem;
  border-bottom: 1px solid #30363d;
  margin-bottom: 2rem;
}
.hero-avatar {
  position: relative;
  width: 80px;
  height: 80px;
  margin: 0 auto 1rem;
}
.avatar-fallback {
  position: absolute;
  inset: 0;
}
.avatar-img {
  position: absolute;
  inset: 0;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  z-index: 1;
}
.hero-name {
  font-size: 1.6rem;
  font-weight: 600;
  color: #e6edf3;
  margin-bottom: 0.6rem;
}
.hero-bio {
  color: #8b949e;
  font-size: 0.95rem;
  max-width: 500px;
  margin: 0 auto 1.5rem;
  line-height: 1.6;
}
.hero-stats {
  display: flex;
  justify-content: center;
  gap: 2.5rem;
  margin-bottom: 1.5rem;
}
.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.stat-num {
  font-size: 1.3rem;
  font-weight: 600;
  color: #e6edf3;
}
.stat-label {
  font-size: 0.75rem;
  color: #8b949e;
  margin-top: 0.15rem;
}
.hero-links {
  display: flex;
  justify-content: center;
  gap: 2rem;
  flex-wrap: wrap;
}
.hero-link {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  color: #8b949e;
  font-size: 0.85rem;
  text-decoration: none;
}
.hero-link[href]:hover {
  color: #60a5fa;
}
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.section-header h2 {
  font-size: 1.15rem;
  font-weight: 600;
  color: #e6edf3;
}
.view-all {
  font-size: 0.85rem;
  color: #60a5fa;
  text-decoration: none;
}
.view-all:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .hero-stats {
    gap: 1.5rem;
  }
  .hero-links {
    gap: 1.2rem;
  }
}
</style>
