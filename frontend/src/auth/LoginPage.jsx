import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useAuth } from './AuthProvider'

export default function LoginPage() {
  const [creds, setCreds] = useState({ username: '', password: '' })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const auth = useAuth()
  const navigate = useNavigate()

  const submit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    try {
      await auth.login(creds)
      navigate('/')
    } catch (err) {
      setError(err.message || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-50 to-yellow-50">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="bg-white p-8 rounded-xl shadow-lg w-full max-w-md">
        <div className="text-center mb-4">
          <img src="/logo.png" alt="Uzuri" className="mx-auto w-24 h-24 object-contain" />
          <h2 className="text-2xl font-bold">Sign in</h2>
          <p className="text-sm text-gray-500">Student login with student number</p>
        </div>

        <form onSubmit={submit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium">Student Number</label>
            <input value={creds.username} onChange={(e) => setCreds({ ...creds, username: e.target.value })} className="mt-1 block w-full rounded-md border p-2" />
          </div>
          <div>
            <label className="block text-sm font-medium">Password</label>
            <input type="password" value={creds.password} onChange={(e) => setCreds({ ...creds, password: e.target.value })} className="mt-1 block w-full rounded-md border p-2" />
          </div>

          {error && <div className="text-sm text-red-600">{error}</div>}

          <button disabled={loading} className="w-full bg-blue-600 text-white p-2 rounded-md">{loading ? 'Signing in...' : 'Sign in'}</button>
        </form>
      </motion.div>
    </div>
  )
}
