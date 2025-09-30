import React, { createContext, useContext, useEffect, useState } from 'react'
import api from '../api/client'
import { useNavigate } from 'react-router-dom'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem('uzuri_token'))
  const [user, setUser] = useState(null)
  const navigate = useNavigate()

  // If a token exists on startup, configure axios header and fetch user
  useEffect(() => {
    if (token) {
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`
      // Fetch current user
      fetchMe()
    }
  }, [token])

  async function login(username, password) {
    // Default login endpoint — adjust if your backend uses a different path
    const path = '/api/auth/login/'
    try {
      const res = await api.post(path, { username, password })
      const t = res.data && (res.data.token || res.data.access)
      if (t) {
        localStorage.setItem('uzuri_token', t)
        setToken(t)
        api.defaults.headers.common['Authorization'] = `Bearer ${t}`
      }
      // Optionally set user from response
      if (res.data.user) setUser(res.data.user)
      return { ok: true, data: res.data }
    } catch (err) {
      return { ok: false, error: err.response ? err.response.data : err.message }
    }
  }

  async function register(payload) {
    try {
      const res = await api.post('/api/auth/register/', payload)
      return { ok: true, data: res.data }
    } catch (err) {
      return { ok: false, error: err.response ? err.response.data : err.message }
    }
  }

  async function fetchMe() {
    try {
      const res = await api.get('/api/auth/me/')
      setUser(res.data)
      return { ok: true, data: res.data }
    } catch (err) {
      // token may be invalid
      setUser(null)
      return { ok: false, error: err.response ? err.response.data : err.message }
    }
  }

  function logout() {
    localStorage.removeItem('uzuri_token')
    setToken(null)
    setUser(null)
    delete api.defaults.headers.common['Authorization']
    navigate('/login')
  }

  const value = { token, user, login, logout, register, fetchMe }
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  return useContext(AuthContext)
}
