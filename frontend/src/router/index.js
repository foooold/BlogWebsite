import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import Blog from '@/views/Blog.vue'
import PostDetail from '@/views/PostDetail.vue'
import Archive from '@/views/Archive.vue'
import About from '@/views/About.vue'

const routes = [
  { path: '/', name: 'home', component: Home, meta: { title: 'Frank Du 的个人空间' } },
  { path: '/blog', name: 'blog', component: Blog, meta: { title: '博客' } },
  { path: '/blog/:slug', name: 'post-detail', component: PostDetail },
  { path: '/archive', name: 'archive', component: Archive, meta: { title: '归档' } },
  { path: '/about', name: 'about', component: About, meta: { title: '关于 - Frank Du 的个人空间' } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.afterEach((to) => {
  if (to.meta.title) {
    document.title = to.meta.title
  }
})

export default router
