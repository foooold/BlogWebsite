<template>
  <div id="app-container">
    <nav class="nav-bar">
      <div class="nav-inner">
        <div class="nav-left">
          <router-link to="/" class="nav-brand">
            <svg width="22" height="22" viewBox="0 0 16 16" fill="currentColor">
            <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
            Frank's Blog
          </router-link>
        </div>
        <div class="nav-right">
          <SearchBar />
          <span class="nav-sep"></span>
          <router-link to="/">首页</router-link>
          <router-link to="/blog">博客</router-link>
          <router-link to="/archive">归档</router-link>
          <router-link to="/about">关于</router-link>
        </div>
      </div>
    </nav>
    <main class="main-content">
      <router-view />
    </main>
    <footer class="site-footer">
      <div class="footer-inner">
        <span>&copy; 2026 Frank's Blog</span>
        <span class="footer-dot">·</span>
        <span>Powered by Vue 3 + Vite + Django</span>
      </div>
    </footer>
  </div>
</template>

<script setup>
import SearchBar from '@/components/SearchBar.vue'
</script>

<style scoped>
#app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.nav-bar {
  background: #161b22;
  border-bottom: 1px solid #30363d;
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
.nav-brand {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.95rem;
  font-weight: 600;
  color: #e6edf3;
  text-decoration: none;
}
.nav-brand:hover {
  color: #c9d1d9;
}
.nav-brand svg {
  color: #8b949e;
}
.nav-right {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}
.nav-sep {
  width: 1px;
  height: 20px;
  background: #30363d;
  margin: 0 0.5rem;
}
.nav-right a {
  padding: 0.35rem 0.7rem;
  font-size: 0.85rem;
  color: #c9d1d9;
  text-decoration: none;
  border-radius: 6px;
}
.nav-right a:hover {
  background: #21262d;
  color: #e6edf3;
}
.nav-right a.router-link-exact-active {
  background: #21262d;
  color: #e6edf3;
}
.main-content {
  flex: 1;
  padding: 0 0 3rem;
}
.site-footer {
  border-top: 1px solid #30363d;
  padding: 1.5rem 1rem;
  margin-top: auto;
}
.footer-inner {
  max-width: 1060px;
  margin: 0 auto;
  text-align: center;
  font-size: 0.8rem;
  color: #484f58;
}
.footer-dot {
  margin: 0 0.4rem;
}
</style>
