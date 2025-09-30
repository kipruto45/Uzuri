import axios from 'axios'

const base = import.meta.env.VITE_API_BASE || ''

const api = axios.create({
  baseURL: base
})

// Attach token from localStorage if present
const token = typeof window !== 'undefined' ? localStorage.getItem('uzuri_token') : null
if (token) api.defaults.headers.common['Authorization'] = `Bearer ${token}`

export function resolveApiUrl(path){
  if (!path) return path
  if (path.startsWith('http')) return path
  if (base) return base.replace(/\/$/, '') + path
  return path
}

export default api
