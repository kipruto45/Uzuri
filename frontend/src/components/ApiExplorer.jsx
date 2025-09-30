import React, { useState } from 'react'
import axios from 'axios'

const DEFAULT_BASE = import.meta.env.VITE_API_BASE || ''

export default function ApiExplorer() {
  const [path, setPath] = useState('/api/')
  const [method, setMethod] = useState('GET')
  const [body, setBody] = useState('')
  const [response, setResponse] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const base = DEFAULT_BASE

  async function send() {
    setLoading(true)
    setError(null)
    setResponse(null)

    const url = path.startsWith('http') ? path : (base ? base.replace(/\/$/, '') + path : path)

    try {
      const opts = { method, url }
      if (method !== 'GET' && body) {
        try { opts.data = JSON.parse(body) } catch (e) { opts.data = body }
      }
      const res = await axios(opts)
      setResponse({ status: res.status, data: res.data })
    } catch (err) {
      if (err.response) setError({ status: err.response.status, data: err.response.data })
      else setError({ message: err.message })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="api-explorer">
      <h2>API Explorer</h2>
      <p>Enter an API path (e.g. <code>/api/attachments/</code>) and click Send. The dev server proxies <code>/api</code> to your backend at <code>http://localhost:8000</code> by default.</p>

      <div className="form-row">
        <label>Method</label>
        <select value={method} onChange={e => setMethod(e.target.value)}>
          <option>GET</option>
          <option>POST</option>
          <option>PUT</option>
          <option>PATCH</option>
          <option>DELETE</option>
        </select>

        <label>Path</label>
        <input value={path} onChange={e => setPath(e.target.value)} />
      </div>

      <div className="form-row">
        <label>Body (JSON)</label>
        <textarea value={body} onChange={e => setBody(e.target.value)} placeholder='{"key":"value"}' />
      </div>

      <div className="form-row">
        <button onClick={send} disabled={loading}>{loading ? 'Sending...' : 'Send'}</button>
      </div>

      <div className="response">
        <h3>Response</h3>
        {error && (
          <pre className="error">{JSON.stringify(error, null, 2)}</pre>
        )}
        {response && (
          <pre className="ok">{JSON.stringify(response, null, 2)}</pre>
        )}
        {!response && !error && <div className="hint">No response yet.</div>}
      </div>
    </div>
  )
}
