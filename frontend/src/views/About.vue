<template>
  <div class="about-page">
    <PageHeader title="关于" description="关于我和这个博客" />

    <div class="about-grid">
      <div class="about-main">
        <section class="about-section">
          <h3>关于我</h3>
          <p>
            我是 Frank，一名上海在读本科生，主修数据科学与大数据技术专业。
            <br>
            你可以在此网页获取我的联系方式。
          </p>
        </section>

        <section class="about-section">
          <h3>关于这个博客</h3>
          <p style="white-space: pre-line;">
            如果你问我为什么要搭这个博客，我会想半天然后敷衍你说不知道。
            <br>
            其实好几年前就有想过建一个网站，学学项目写写日志然后美美上传，但那时候还没接触 Git，<!--
            -->甚至连 cpp 都才学到 include iostream，这个想法最后当然也是美美泡汤。
            <br>
            后来大学进入了一个计算机专业，大语言模型迭代的也越来越快，各个大厂都开始<!--
            -->推出自家的 Harness。直到上周 —— 2026-07-18，我偶然发现 DeepSeek-V4 开始了灰度<!--
            -->测试而且还支持接入 Claude code，那为何不以此为契机让 Agent 协助我实<!--
            -->现几年前的想法呢。
            <br>
            知与行不应该分离，实践本身就是学习的一部分甚至可以更好得将知识转化为成果。在这次实践中本博客<!--
            -->于 2026-07-21 成功部署上线，我计划把这个博客作为记录我的学习过程和日常的空间，我会经常<!--
            -->发布项目更新日志也会分享一些个人想法和心得，希望我能持续更新这个项目 ٩(ˊᗜˋ*)و
            <br>
            所以...
            <br>
            什么？你问我为什么要搭这个博客？不知道
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
              <span class="contact-label">Repository</span>
              <span class="contact-value">
                <a href="https://github.com/foooold/BlogWebsite" target="_blank">/BlogWebstie</a>
              </span>
            </li>

            <li>
              <span class="contact-label">Location</span>
              <span class="contact-value">中国 上海</span>
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
