<template>
  <div class="home-page">
    <section class="hero-mobile">
      <div class="hero-mobile-avatar">
        <svg width="80" height="80" viewBox="0 0 80 80" fill="none" class="hero-mobile-fallback">
          <circle cx="40" cy="40" r="40" fill="#30363d"/>
          <circle cx="40" cy="32" r="14" fill="#8b949e"/>
          <ellipse cx="40" cy="66" rx="24" ry="12" fill="#8b949e"/>
        </svg>
        <img v-show="!showFallback" :src="avatarUrl" alt="Frank Du" class="hero-mobile-img" @error="onAvatarError" />
      </div>
      <h1 class="hero-mobile-name">Frank Du</h1>
      <p class="hero-mobile-bio">欢迎来到我的个人博客！</p>
      <div class="hero-mobile-stats">
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
      <div class="hero-mobile-links">
        <a href="https://github.com/foooold" target="_blank" class="hero-mobile-link">
          <svg width="18" height="18" viewBox="0 0 16 16" fill="currentColor"><path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
          GitHub
        </a>
        <span class="hero-mobile-link">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
          <polyline points="22,6 12,13 2,6"/>
          </svg>
          1474036970@qq.com
        </span>
      </div>
    </section>

    <section class="recent-posts">
      <div class="posts-layout">
        <div class="post-grid">
          <div class="section-header">
            <h2>最新文章</h2>
            <router-link to="/blog" class="view-all">查看全部 →</router-link>
          </div>
          <BlogCard v-for="post in recentPosts" :key="post.id" :post="post" />
        </div>
        <div class="sidebar">
          <aside class="profile-card">
            <div class="profile-avatar">
              <svg width="64" height="64" viewBox="0 0 80 80" fill="none" class="avatar-fallback">
                <circle cx="40" cy="40" r="40" fill="#30363d"/>
                <circle cx="40" cy="32" r="14" fill="#8b949e"/>
                <ellipse cx="40" cy="66" rx="24" ry="12" fill="#8b949e"/>
              </svg>
              <img v-show="!showFallback" :src="avatarUrl" alt="Frank Du" class="avatar-img" @error="onAvatarError" />
            </div>
            <h3 class="profile-name">Frank Du</h3>
            <p class="profile-bio">欢迎来到我的个人博客！</p>
            <div class="profile-stats">
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
            <div class="profile-links">
              <a href="https://github.com/foooold" target="_blank" class="profile-link">
                <svg width="18" height="18" viewBox="0 0 16 16" fill="currentColor"><path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
                GitHub
              </a>
              <span class="profile-link">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                <polyline points="22,6 12,13 2,6"/>
                </svg>
                1474036970@qq.com
              </span>
            </div>
          </aside>
          <aside class="changelog-card">
            <h3 class="changelog-title">更新日志</h3>
            <div class="changelog-list">
              <div v-for="entry in changelog" :key="entry.version" class="changelog-entry">
                <div class="changelog-version">
                  <span class="changelog-ver">v{{ entry.version }}</span>
                  <span class="changelog-date">{{ entry.date }}</span>
                </div>
                <ul class="changelog-items">
                  <li v-for="item in changelogItems(entry)" :key="item" class="changelog-item" v-html="md.renderInline(item)"></li>
                </ul>
              </div>
            </div>
          </aside>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import MarkdownIt from 'markdown-it'
import { getArticles, getTags, getChangelog } from '@/api'
import BlogCard from '@/components/BlogCard.vue'

const md = new MarkdownIt()

const avatarUrl = '/static/avatar.png'
const allPosts = ref([])
const allTags = ref([])

const recentPosts = computed(() => allPosts.value.slice(0, 5))

const changelog = ref([])

function changelogItems(entry) {
  const sections = entry.sections || {}
  return [].concat(
    sections['Features'] || [],
    sections['Bug Fixes'] || [],
    sections['Improvements'] || [],
  )
}

onMounted(async () => {
  try {
    const [articles, tags] = await Promise.all([getArticles(), getTags()])
    allPosts.value = articles
    allTags.value = tags
  } catch (e) {
    console.error('Failed to load data:', e)
  }
  try {
    const res = await getChangelog()
    changelog.value = res.entries || []
  } catch (e) {
    console.error('Failed to load changelog:', e)
  }
})

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
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem 4rem;
}
.hero-mobile {
  display: none;
}
.hero-mobile-avatar {
  position: relative;
  width: 80px;
  height: 80px;
  margin: 0 auto 1rem;
}
.hero-mobile-fallback {
  position: absolute;
  inset: 0;
}
.hero-mobile-img {
  position: absolute;
  inset: 0;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  z-index: 1;
}
.hero-mobile-name {
  font-size: 1.6rem;
  font-weight: 600;
  color: #e6edf3;
  margin-bottom: 0.6rem;
}
.hero-mobile-bio {
  color: #8b949e;
  font-size: 0.95rem;
  max-width: 500px;
  margin: 0 auto 1.5rem;
  line-height: 1.6;
}
.hero-mobile-stats {
  display: flex;
  justify-content: center;
  gap: 2.5rem;
  margin-bottom: 1.5rem;
}
.hero-mobile-links {
  display: flex;
  justify-content: center;
  gap: 2rem;
  flex-wrap: wrap;
}
.hero-mobile-link {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  color: #8b949e;
  font-size: 0.85rem;
  text-decoration: none;
}
.hero-mobile-link[href]:hover {
  color: #60a5fa;
}
.profile-avatar {
  position: relative;
  width: 64px;
  height: 64px;
  margin: 0 auto 0.75rem;
}
.avatar-fallback {
  position: absolute;
  inset: 0;
}
.avatar-img {
  position: absolute;
  inset: 0;
  width: 64px;
  height: 64px;
  border-radius: 50%;
  object-fit: cover;
  z-index: 1;
}
.posts-layout {
  display: flex;
  gap: 2rem;
  align-items: flex-start;
}
.post-grid {
  flex: 1;
  min-width: 800;
  max-width: 1200px;
}
.sidebar {
  flex-shrink: 0;
  min-width: 270px;
  max-width: 340px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.profile-card {
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 8px;
  margin-top: 45px;
  padding: 1.5rem 1.25rem;
  text-align: center;
}
.profile-name {
  font-size: 1.25rem;
  font-weight: 600;
  color: #e6edf3;
  margin-bottom: 0.5rem;
}
.profile-bio {
  color: #8b949e;
  font-size: 0.85rem;
  margin-bottom: 1.25rem;
  line-height: 1.5;
}
.profile-stats {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin-bottom: 1.25rem;
  padding-bottom: 1.25rem;
  border-bottom: 1px solid #30363d;
}
.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.stat-num {
  font-size: 1.15rem;
  font-weight: 600;
  color: #e6edf3;
}
.stat-label {
  font-size: 0.7rem;
  color: #8b949e;
  margin-top: 0.1rem;
}
.profile-links {
  display: flex;
  justify-content: center;
  gap: 1rem;
}
.profile-link {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  color: #8b949e;
  font-size: 0.8rem;
  text-decoration: none;
}
.profile-link[href]:hover {
  color: #60a5fa;
}
.changelog-card {
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 8px;
  padding: 1rem 1rem;
  text-align: left;
}
.changelog-title {
  font-size: 0.95rem;
  font-weight: 600;
  color: #e6edf3;
  margin-bottom: 0.75rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #30363d;
}
.changelog-list {
  max-height: 420px;
  overflow-y: auto;
}
.changelog-entry {
  margin-bottom: 0.75rem;
}
.changelog-entry:last-child {
  margin-bottom: 0;
}
.changelog-version {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
  margin-bottom: 0.3rem;
}
.changelog-ver {
  font-size: 0.8rem;
  font-weight: 600;
  color: #60a5fa;
}
.changelog-date {
  font-size: 0.7rem;
  color: #484f58;
}
.changelog-items {
  list-style: none;
  padding: 0;
  margin: 0;
}
.changelog-item {
  font-size: 0.75rem;
  color: #8b949e;
  line-height: 1.5;
  padding: 0.15rem 0;
}
.changelog-item::before {
  content: '• ';
  color: #484f58;
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
  .hero-mobile {
    display: block;
    text-align: center;
    padding: 2rem 1rem;
    border-bottom: 1px solid #30363d;
    margin-bottom: 2rem;
  }
  .hero-mobile-stats {
    gap: 1.5rem;
  }
  .hero-mobile-links {
    gap: 1.2rem;
  }
  .sidebar {
    display: none;
  }
  .home-page {
    padding: 1rem 1rem;  /* 你要的值 */
  }
}
</style>
