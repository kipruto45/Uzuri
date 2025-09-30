import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import api, { resolveApiUrl } from '../api/client'

export default function CrudPage(){
  const { name } = useParams()
  const [url, setUrl] = useState(null)
  const [items, setItems] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)
  const [selected, setSelected] = useState(null)
  const [payload, setPayload] = useState('{}')

  useEffect(()=>{
    let mounted = true
    async function load(){
      setLoading(true)
      setError(null)
      try{
        const root = await api.get('/api/')
        const r = root.data[name]
        if (!r) throw new Error('Resource not found on API root')
        const resolved = resolveApiUrl(r)
        if (!mounted) return
        setUrl(resolved)
        const res = await api.get(resolved)
        if (!mounted) return
        setItems(res.data)
      }catch(err){
        setError(err.response ? err.response.data : err.message)
      }finally{ if (mounted) setLoading(false) }
    }
    load()
    return ()=>{ mounted = false }
  },[name])

  async function refresh(){
    if (!url) return
    setLoading(true); setError(null)
    try{ const res = await api.get(url); setItems(res.data) }catch(err){ setError(err.response ? err.response.data : err.message) }finally{ setLoading(false) }
  }

  async function viewItem(item){
    // allow passing detailed url if available
    const itemUrl = item.url || (url.endsWith('/') ? `${url}${item.id}/` : `${url}/${item.id}/`)
    try{
      const res = await api.get(resolveApiUrl(itemUrl))
      setSelected(res.data)
    }catch(err){ setError(err.response ? err.response.data : err.message) }
  }

  async function createItem(e){
    e.preventDefault()
    setError(null)
    let data
    try{ data = JSON.parse(payload) } catch(err){ setError('Invalid JSON'); return }
    try{
      await api.post(url, data)
      setPayload('{}')
      await refresh()
    }catch(err){ setError(err.response ? err.response.data : err.message) }
  }

  async function deleteItem(item){
    const itemUrl = item.url || (url.endsWith('/') ? `${url}${item.id}/` : `${url}/${item.id}/`)
    try{
      await api.delete(resolveApiUrl(itemUrl))
      if (selected && selected.id === item.id) setSelected(null)
      await refresh()
    }catch(err){ setError(err.response ? err.response.data : err.message) }
  }

  return (
    <div>
      <h2>CRUD: {name}</h2>
      {error && <pre style={{color:'crimson'}}>{JSON.stringify(error,null,2)}</pre>}
      {loading && <div>Loading…</div>}
      {!loading && url && (
        <div style={{display:'flex',gap:20,alignItems:'flex-start'}}>
          <div style={{flex:1}}>
            <h3>List</h3>
            <button onClick={refresh}>Refresh</button>
            {Array.isArray(items) ? (
              <ul>
                {items.map(it => (
                  <li key={it.id || it.url || JSON.stringify(it)} style={{marginBottom:8}}>
                    <button onClick={()=>viewItem(it)}>View</button>
                    <button onClick={()=>deleteItem(it)} style={{marginLeft:8}}>Delete</button>
                    <span style={{marginLeft:8}}>{it.id ? `#${it.id}` : ''} {it.title || it.name || it.email || JSON.stringify(it)}</span>
                  </li>
                ))}
              </ul>
            ) : <pre>{JSON.stringify(items,null,2)}</pre>}
          </div>

          <div style={{flex:1}}>
            <h3>Create</h3>
            <form onSubmit={createItem}>
              <textarea value={payload} onChange={e=>setPayload(e.target.value)} style={{width:'100%',height:200,fontFamily:'monospace'}} />
              <div style={{marginTop:8}}>
                <button type="submit">Create</button>
              </div>
            </form>

            <h3>Selected</h3>
            {selected ? <pre style={{whiteSpace:'pre-wrap'}}>{JSON.stringify(selected,null,2)}</pre> : <div>No item selected</div>}
          </div>
        </div>
      )}
    </div>
  )
}
