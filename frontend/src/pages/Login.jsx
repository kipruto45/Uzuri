import React, { useState } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { useNavigate } from 'react-router-dom'

export default function Login(){
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)
  const auth = useAuth()
  const navigate = useNavigate()

  async function submit(e){
    e.preventDefault()
    setError(null)
    const res = await auth.login(username, password)
    if (res.ok) navigate('/attachments')
    else setError(res.error || 'Login failed')
  }

  return (
    <div style={{maxWidth:440}}>
      <h2>Login</h2>
      <form onSubmit={submit}>
        <div style={{marginBottom:8}}>
          <label>Username</label>
          <input value={username} onChange={e=>setUsername(e.target.value)} />
        </div>
        <div style={{marginBottom:8}}>
          <label>Password</label>
          <input type="password" value={password} onChange={e=>setPassword(e.target.value)} />
        </div>
        <button type="submit">Login</button>
      </form>
      {error && <pre style={{color:'crimson'}}>{JSON.stringify(error,null,2)}</pre>}
    </div>
  )
}
