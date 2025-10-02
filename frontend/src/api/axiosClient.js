import axios from 'axios'

// support both Vite and CRA env var names
// Prefer commonly-used env var names; safe for Jest and Node environments
const API_BASE = process.env.VITE_API_BASE || process.env.VITE_API_BASE_URL || process.env.REACT_APP_API_BASE_URL || '/api/'

const axiosClient = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
})

// Helper to read tokens stored in localStorage in a consistent shape
function getStoredTokens() {
  try {
    const raw = localStorage.getItem('uzuri_auth')
    if (!raw) return null
    return JSON.parse(raw)
  } catch (e) {
    return null
  }
}

// Attach access token if available
axiosClient.interceptors.request.use((config) => {
  const tokens = getStoredTokens()
  if (tokens?.access) {
    config.headers = config.headers || {}
    config.headers.Authorization = `Bearer ${tokens.access}`
  }
  return config
})

let isRefreshing = false
let failedQueue = []

const processQueue = (error, token = null) => {
  failedQueue.forEach((prom) => {
    if (error) prom.reject(error)
    else prom.resolve(token)
  })
  failedQueue = []
}

axiosClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const originalRequest = error.config
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      const tokens = getStoredTokens()
      if (!tokens?.refresh) {
        return Promise.reject(error)
      }

      if (isRefreshing) {
        return new Promise(function (resolve, reject) {
          failedQueue.push({ resolve, reject })
        })
          .then((token) => {
            originalRequest.headers.Authorization = 'Bearer ' + token
            return axiosClient(originalRequest)
          })
          .catch((err) => Promise.reject(err))
      }

      originalRequest._retry = true
      isRefreshing = true

      const refreshClient = axios.create({ baseURL: API_BASE })
      return refreshClient
        .post('/auth/refresh/', { refresh: tokens.refresh })
        .then((res) => {
          const newAccess = res.data?.access || res.data?.token
          if (!newAccess) throw new Error('No access token in refresh response')
          // update stored tokens (keep refresh)
          const updated = { ...tokens, access: newAccess }
          localStorage.setItem('uzuri_auth', JSON.stringify(updated))
          axiosClient.defaults.headers.common.Authorization = 'Bearer ' + newAccess
          originalRequest.headers.Authorization = 'Bearer ' + newAccess
          processQueue(null, newAccess)
          return axiosClient(originalRequest)
        })
        .catch((err) => {
          processQueue(err, null)
          // on refresh failure, clear storage
          localStorage.removeItem('uzuri_auth')
          return Promise.reject(err)
        })
        .finally(() => {
          isRefreshing = false
        })
    }
    return Promise.reject(error)
  }
)

export default axiosClient
