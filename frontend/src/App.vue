<template>
  <div id="app-container">
    <!-- ===== PC 导航栏 ===== -->
    <nav v-if="!isMobile" class="nav-bar">
      <div class="nav-inner">
        <div class="nav-left">
          <router-link to="/" class="nav-brand">
            <img src="/static/avatar.png" alt="Frank's Blog" class="nav-avatar" />
            <span class="brand-text">Frank's Blog</span>
          </router-link>
        </div>
        <div class="nav-right">
          <SearchBar />
          <ThemeToggle />
          <span class="nav-sep"></span>
          <router-link to="/">首页</router-link>
          <router-link to="/blog">博客</router-link>
          <router-link to="/archive">归档</router-link>
          <router-link to="/about">关于</router-link>
        </div>
      </div>
    </nav>

    <!-- ===== 移动端导航栏 ===== -->
    <nav v-else class="nav-bar mobile-nav-bar">
      <div class="nav-inner mobile-nav-inner">
        <router-link to="/" class="nav-brand mobile-brand">
          <img src="/static/avatar.png" alt="Frank's Blog" class="nav-avatar" />
          <span class="brand-text mobile-brand-text">Blog</span>
        </router-link>
        <button class="hamburger-btn" @click="openDrawer" aria-label="菜单">
          <span></span><span></span><span></span>
        </button>
      </div>
    </nav>

    <!-- ===== 移动端遮罩层 ===== -->
    <div v-if="isMobile && drawerOpen" class="drawer-overlay" :style="{ top: drawerTop + 'px', height: drawerHeight + 'px' }" @click="closeDrawer"></div>

    <!-- ===== 移动端侧滑抽屉 ===== -->
    <div v-if="isMobile" class="drawer" :class="{ open: drawerOpen }" :style="{ top: drawerTop + 'px', height: drawerHeight + 'px' }">
      <div class="drawer-header">
        <span class="drawer-title">导航</span>
        <div class="drawer-actions">
          <ThemeToggle />
          <button class="drawer-close" @click="closeDrawer" aria-label="关闭">
            <svg width="20" height="20" viewBox="0 0 16 16" fill="currentColor"><path fill-rule="evenodd" d="M3.72 3.72a.75.75 0 011.06 0L8 6.94l3.22-3.22a.75.75 0 111.06 1.06L9.06 8l3.22 3.22a.75.75 0 11-1.06 1.06L8 9.06l-3.22 3.22a.75.75 0 01-1.06-1.06L6.94 8 3.72 4.78a.75.75 0 010-1.06z"/></svg>
          </button>
        </div>
      </div>

      <div class="drawer-search">
        <SearchBar />
      </div>

      <router-link to="/" class="drawer-link" :class="{ active: $route.path === '/' }" @click="closeDrawer">
        <svg width="18" height="18" viewBox="0 0 16 16" fill="currentColor"><path fill-rule="evenodd" d="M7.823.127a.25.25 0 01.354 0l6.146 5.804a.25.25 0 01-.093.423L7.5 7.87a.25.25 0 01-.223-.036l-4.992-3.66a.25.25 0 01.039-.425L7.823.127zM1.5 14.654V6.729a.25.25 0 01.364-.224l4.496 1.94a.25.25 0 01.14.138l2.378 5.357a.25.25 0 01-.22.368H1.777a.25.25 0 01-.251-.192 5.53 5.53 0 01-.026-.462zM14.5 14.654V6.729a.25.25 0 00-.364-.224l-4.496 1.94a.25.25 0 00-.14.138l-2.378 5.357a.25.25 0 00.22.368h5.38c.16 0 .292-.124.252-.28a5.396 5.396 0 00-.027-.374z"/></svg>
        首页
      </router-link>
      <router-link to="/blog" class="drawer-link" :class="{ active: $route.path.startsWith('/blog') }" @click="closeDrawer">
        <svg width="18" height="18" viewBox="0 0 16 16" fill="currentColor"><path d="M0 1.75A.75.75 0 01.75 1h4.253c1.227 0 2.317.59 3 1.501A3.744 3.744 0 0111.006 1h4.245a.75.75 0 01.75.75v10.5a.75.75 0 01-.75.75h-4.507a2.25 2.25 0 00-1.591.659l-.622.621a.75.75 0 01-1.06 0l-.622-.621A2.25 2.25 0 005.258 13H.75a.75.75 0 01-.75-.75V1.75z"/></svg>
        博客
      </router-link>
      <router-link to="/archive" class="drawer-link" :class="{ active: $route.path === '/archive' }" @click="closeDrawer">
        <svg width="18" height="18" viewBox="0 0 16 16" fill="currentColor"><path fill-rule="evenodd" d="M.75 2a.75.75 0 000 1.5H2v9.75A2.75 2.75 0 004.75 16h6.5A2.75 2.75 0 0014 13.25V3.5h1.25a.75.75 0 000-1.5H.75zM14 3.5v.75H2V3.5h12zm-1.5 2.25H3.5v7.5c0 .69.56 1.25 1.25 1.25h6.5c.69 0 1.25-.56 1.25-1.25v-7.5z"/></svg>
        归档
      </router-link>
      <router-link to="/about" class="drawer-link" :class="{ active: $route.path === '/about' }" @click="closeDrawer">
        <svg width="18" height="18" viewBox="0 0 16 16" fill="currentColor"><path fill-rule="evenodd" d="M10.5 5a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0zm.061 3.073a4 4 0 10-5.123 0 6.004 6.004 0 00-3.431 5.142.75.75 0 001.498.07 4.5 4.5 0 018.99 0 .75.75 0 101.498-.07 6.005 6.005 0 00-3.432-5.142z"/></svg>
        关于
      </router-link>

      <div class="drawer-footer">
        <span>&copy; 2026 Frank's Blog</span>
      </div>
    </div>

    <main class="main-content">
      <router-view />
    </main>
    <footer class="site-footer">
      <div class="footer-inner">
        <span>&copy; 2026 Frank's Blog</span>
        <span class="footer-dot">·</span>
        <span>Powered by Vue 3 + Vite + Django</span>
        <br />
        <a href="https://beian.miit.gov.cn/" target="_blank" rel="noopener" class="icp-link">沪ICP备XXXXXXXX号-1</a>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, watch, onBeforeUnmount } from 'vue'
import { useRoute } from 'vue-router'
import SearchBar from '@/components/SearchBar.vue'
import ThemeToggle from '@/components/ThemeToggle.vue'
import { useMediaQuery } from '@/composables/useMediaQuery'

const route = useRoute()
const isMobile = useMediaQuery()
const drawerOpen = ref(false)
const drawerTop = ref(0)
const drawerHeight = ref(0)

function openDrawer() {
  drawerTop.value = window.scrollY
  drawerHeight.value = window.innerHeight
  drawerOpen.value = true
  document.body.style.overflow = 'hidden'
}

function closeDrawer() {
  drawerOpen.value = false
  document.body.style.overflow = ''
}

watch(() => route.path, () => closeDrawer())

onBeforeUnmount(() => {
  document.body.style.overflow = ''
})
</script>

<style scoped>
/* ===== 通用 ===== */
#app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow-x: clip;
}
.nav-bar {
  background: var(--bg-default);
  border-bottom: 1px solid var(--border-default);
  position: sticky;
  top: 0;
  z-index: 10;
}
.nav-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 2rem;
  height: 52px;
}
.nav-left {
  display: flex;
  align-items: center;
  height: 52px;
}
.nav-brand {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: var(--fg-strong);
  text-decoration: none;
}
.brand-text {
  font-family: 'Times New Roman', serif;
  color: var(--fg-default);
  font-size: 18px;
  letter-spacing: 0.5px;
  padding-top: 5px;
}
.nav-brand:hover .brand-text { color: var(--fg-strong); }
.nav-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid var(--border-default);
}
.nav-right {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}
.nav-right :deep(.theme-toggle) { margin-left: 0.4rem; }
.nav-sep {
  width: 1px;
  height: 20px;
  background: var(--border-default);
  margin: 0 0.5rem;
}
.nav-right a {
  padding: 0.35rem 0.7rem;
  font-size: 0.85rem;
  color: var(--fg-default);
  text-decoration: none;
  border-radius: 6px;
}
.nav-right a:hover {
  background: var(--control-hover-bg);
  color: var(--control-hover-fg);
}
.nav-right a.router-link-exact-active {
  background: var(--control-active-bg);
  color: var(--control-hover-fg);
}
.main-content {
  flex: 1;
  padding: 0 0 3rem;
}
.site-footer {
  border-top: 1px solid var(--border-default);
  padding: 1.5rem 1rem;
  margin-top: auto;
}
.footer-inner {
  max-width: 1060px;
  margin: 0 auto;
  text-align: center;
  font-size: 0.8rem;
  color: var(--fg-subtle);
}
.footer-dot { margin: 0 0.4rem; }
.icp-link { color: var(--fg-subtle); text-decoration: none; }
.icp-link:hover { color: var(--fg-muted); text-decoration: underline; }

/* ===== 移动端导航栏 ===== */
.mobile-nav-bar {
  height: 48px;
}
.mobile-nav-inner {
  height: 48px;
  padding: 0 1rem;
}
.mobile-brand-text {
  font-size: 22px;
}
.mobile-brand svg {
  width: 24px;
  height: 24px;
}
.hamburger-btn {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 4px;
  width: 36px;
  height: 36px;
  padding: 6px;
  background: transparent;
  border: 1px solid var(--border-default);
  border-radius: 6px;
  cursor: pointer;
}
.hamburger-btn span {
  display: block;
  height: 2px;
  background: var(--fg-default);
  border-radius: 1px;
}
.hamburger-btn:hover {
  background: var(--control-hover-bg);
  border-color: var(--control-hover-border);
}

/* ===== 抽屉遮罩 ===== */
.drawer-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  background: var(--overlay);
  z-index: 20;
}

/* ===== 侧滑抽屉 ===== */
.drawer {
  position: absolute;
  top: 1000;
  bottom: 0;
  right: -300px;
  width: 300px;
  max-width: 85vw;
  background: var(--bg-default);
  border-left: 1px solid var(--border-default);
  z-index: 30;
  display: flex;
  flex-direction: column;
  transition: right 0.25s ease;
  overflow-y: auto;
}
.drawer.open {
  right: 0;
}
.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.9rem 1rem;
  border-bottom: 1px solid var(--border-muted);
}
.drawer-actions {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}
.drawer-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--fg-strong);
}
.drawer-close {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: transparent;
  border: none;
  color: var(--fg-muted);
  cursor: pointer;
  border-radius: 6px;
}
.drawer-close:hover {
  background: var(--control-hover-bg);
  color: var(--control-hover-fg);
}
.drawer-search {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--border-muted);
}
.drawer-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.85rem 1.2rem;
  font-size: 1.05rem;
  color: var(--fg-default);
  text-decoration: none;
  border-bottom: 1px solid var(--border-muted);
}
.drawer-link svg {
  color: var(--fg-muted);
  flex-shrink: 0;
}
.drawer-link:hover {
  background: var(--control-hover-bg);
  color: var(--control-hover-fg);
}
.drawer-link.active {
  background: var(--control-active-bg);
  color: var(--control-hover-fg);
}
.drawer-link.active svg {
  color: var(--accent);
}
.drawer-footer {
  margin-top: auto;
  padding: 1rem;
  text-align: center;
  font-size: 0.78rem;
  color: var(--fg-subtle);
  border-top: 1px solid var(--border-muted);
}
</style>
