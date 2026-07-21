import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import Blog from '@/views/Blog.vue'
import PostDetail from '@/views/PostDetail.vue'
import Archive from '@/views/Archive.vue'
import About from '@/views/About.vue'

const routes = [
  { path: '/', name: 'home', component: Home },
  { path: '/blog', name: 'blog', component: Blog },
  { path: '/blog/:slug', name: 'post-detail', component: PostDetail },
  { path: '/archive', name: 'archive', component: Archive },
  { path: '/about', name: 'about', component: About },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
