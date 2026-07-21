import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  },
)

export function getHello() {
  return api.get('/hello/')
}

export function getArticles() {
  return api.get('/articles/')
}

export function getArticle(slug) {
  return api.get(`/articles/${slug}/`)
}

export function getTags() {
  return api.get('/tags/')
}

export function searchArticles(query) {
  return api.get('/search/', { params: { q: query } })
}

export default api
