import React, { useState } from 'react'
import api from '../api/client'

export default function AttachmentUpload({ onUploaded }){
  const [file, setFile] = useState(null)
  const [title, setTitle] = useState('')
  const [desc, setDesc] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(null)

  async function submit(e){
    e.preventDefault()
    setError(null)
    setSuccess(null)
    if (!file) { setError('Please select a file'); return }

    const form = new FormData()
    form.append('file', file)
    if (title) form.append('title', title)
    if (desc) form.append('description', desc)

    setLoading(true)
    try{
      const res = await api.post('/api/attachments/', form, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      setSuccess(res.data)
      setFile(null)
      setTitle('')
      setDesc('')
      if (onUploaded) onUploaded()
    }catch(err){
      setError(err.response ? err.response.data : err.message)
    }finally{ setLoading(false) }
  }

  return (
    <form onSubmit={submit} style={{marginBottom:16, padding:12, border:'1px solid #eee', borderRadius:8}}>
      <h3>Upload Attachment</h3>
      <div style={{marginBottom:8}}>
        <label style={{display:'block',fontSize:12}}>File</label>
        <input type="file" onChange={e=>setFile(e.target.files[0]||null)} />
      </div>
      <div style={{marginBottom:8}}>
        <label style={{display:'block',fontSize:12}}>Title</label>
        <input value={title} onChange={e=>setTitle(e.target.value)} />
      </div>
      <div style={{marginBottom:8}}>
        <label style={{display:'block',fontSize:12}}>Description</label>
        <input value={desc} onChange={e=>setDesc(e.target.value)} />
      </div>
      <button type="submit" disabled={loading}>{loading ? 'Uploading…' : 'Upload'}</button>
      {error && <div style={{color:'crimson',marginTop:8}}>{JSON.stringify(error)}</div>}
      {success && <div style={{color:'green',marginTop:8}}>Uploaded</div>}
    </form>
  )
}
