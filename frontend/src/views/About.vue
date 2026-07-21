<template>
  <div class="about-page">
    <PageHeader title="关于" description="关于我和这个博客" />

    <div class="about-grid">
      <div class="about-main">
        <section class="about-section">
          <h3>关于我</h3>
          <p>
            我是 Frank，一名上海在读本科生，主修数据科学与大数据技术专业。
          </p>
          <p>
            你可以在此网页获取我的联系方式。
          </p>
        </section>

        <section class="about-section">
          <h3>关于这个博客</h3>
          <p>
            这个博客是我记录学习过程和分享技术心得的空间。我会在这里发布关于以下主题的文章：
          </p>
          <ul>
            <li>Python 和 Django 的深度应用</li>
            <li>Vue.js 和现代前端开发</li>
            <li>数据库设计和查询优化</li>
            <li>DevOps 和部署实践</li>
            <li>编程语言和系统设计</li>
          </ul>
          <p>
            所有文章都基于实际项目经验，力求提供可操作的代码示例和深入的分析。
          </p>
        </section>

        <section class="about-section">
          <h3>技术栈</h3>
          <div class="skills">
            <div class="skill-category">
              <h4>后端</h4>
              <div class="skill-tags">
                <span class="skill-tag">Python</span>
                <span class="skill-tag">Django</span>
                <span class="skill-tag">DRF</span>
                <span class="skill-tag">PostgreSQL</span>
                <span class="skill-tag">Redis</span>
                <span class="skill-tag">Docker</span>
              </div>
            </div>
            <div class="skill-category">
              <h4>前端</h4>
              <div class="skill-tags">
                <span class="skill-tag">Vue 3</span>
                <span class="skill-tag">JavaScript</span>
                <span class="skill-tag">TypeScript</span>
                <span class="skill-tag">Vite</span>
                <span class="skill-tag">Tailwind CSS</span>
              </div>
            </div>
            <div class="skill-category">
              <h4>工具</h4>
              <div class="skill-tags">
                <span class="skill-tag">Git</span>
                <span class="skill-tag">Linux</span>
                <span class="skill-tag">Nginx</span>
                <span class="skill-tag">GitHub Actions</span>
                <span class="skill-tag">VS Code</span>
              </div>
            </div>
          </div>
        </section>
      </div>

      <aside class="about-sidebar">
        <div class="sidebar-card">
          <h3>联系方式</h3>
          <ul class="contact-list">
            <li>
              <span class="contact-label">Email</span>
              <span class="contact-value">
                <a href="mailto:1474036970@qq.com">1474036970@qq.com</a>
              </span>
            </li>
            <li>
              <span class="contact-label">GitHub</span>
              <span class="contact-value">
                <a href="https://github.com/foooold" target="_blank">github.com/foooold</a>
              </span>
            </li>
            <li>
              <span class="contact-label">Location</span>
              <span class="contact-value">中国</span>
            </li>
          </ul>
        </div>

        <div class="sidebar-card">
          <h3>站点统计</h3>
          <ul class="stats-list">
            <li>
              <span>{{ allPosts.length }}</span>
              <span>篇文章</span>
            </li>
            <li>
              <span>{{ allTags.length }}</span>
              <span>个标签</span>
            </li>
            <li>
              <span>{{ allPosts[0]?.date || '—' }}</span>
              <span>最近更新</span>
            </li>
          </ul>
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getArticles, getTags } from '@/api'
import PageHeader from '@/components/PageHeader.vue'

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
</script>

<style scoped>
.about-page {
  max-width: 960px;
  margin: 0 auto;
  padding: 0 1rem;
}
.about-grid {
  display: grid;
  grid-template-columns: 1fr 260px;
  gap: 2rem;
}
@media (max-width: 700px) {
  .about-grid {
    grid-template-columns: 1fr;
  }
}
.about-section {
  margin-bottom: 2rem;
}
.about-section h3 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #e6edf3;
  margin-bottom: 0.75rem;
  padding-bottom: 0.4rem;
  border-bottom: 1px solid #21262d;
}
.about-section p {
  font-size: 0.9rem;
  color: #c9d1d9;
  line-height: 1.7;
  margin-bottom: 0.6rem;
}
.about-section ul {
  margin: 0.5rem 0;
  padding-left: 1.25rem;
}
.about-section li {
  font-size: 0.9rem;
  color: #c9d1d9;
  line-height: 1.7;
}
.skills {
  display: grid;
  gap: 1rem;
}
.skill-category h4 {
  font-size: 0.85rem;
  color: #8b949e;
  margin-bottom: 0.4rem;
  font-weight: 400;
}
.skill-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}
.skill-tag {
  padding: 0.25rem 0.65rem;
  font-size: 0.8rem;
  color: #c9d1d9;
  background: #21262d;
  border: 1px solid #30363d;
  border-radius: 6px;
}
.about-sidebar {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.sidebar-card {
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 6px;
  padding: 1rem 1.25rem;
}
.sidebar-card h3 {
  font-size: 0.9rem;
  font-weight: 600;
  color: #e6edf3;
  margin-bottom: 0.75rem;
}
.contact-list {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}
.contact-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;
}
.contact-label {
  color: #8b949e;
}
.contact-value {
  color: #c9d1d9;
}
.contact-value a {
  color: #60a5fa;
  text-decoration: none;
}
.contact-value a:hover {
  text-decoration: underline;
}
.stats-list {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.stats-list li {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
  color: #c9d1d9;
}
.stats-list li span:first-child {
  font-weight: 600;
  color: #60a5fa;
}
</style>
