import React, { useEffect, useState } from 'react'
import * as api from './api'
import { useParams } from 'react-router-dom'

const mapping = {
  users: api.listUsers,
  roles: api.listRoles,
  profiles: api.listProfiles,
  programs: api.listPrograms,
  courses: api.listCourses,
}

export default function ResourcePage() {
  const { resource } = useParams()
  const [items, setItems] = useState([])
  useEffect(() => {
    let mounted = true
    const fn = mapping[resource]
    if (!fn) return
    fn().then(r => { if (mounted) setItems(r || []) })
    return () => (mounted = false)
  }, [resource])

  return (
    <div className="p-6">
      <h1 className="text-xl font-medium mb-4">{resource}</h1>
      <ul className="space-y-2">
        {items.map((it) => <li key={it.id} className="p-2 bg-white rounded shadow">{JSON.stringify(it)}</li>)}
      </ul>
    </div>
  )
}
