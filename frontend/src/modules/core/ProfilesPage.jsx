import React, { useEffect, useState } from 'react'
import { listProfiles } from './api'

export default function ProfilesPage() {
  const [profiles, setProfiles] = useState([])
  useEffect(() => { let mounted = true; listProfiles().then(r => { if (mounted) setProfiles(r || []) }); return () => mounted = false }, [])
  return (
    <div className="p-6">
      <h1 className="text-xl font-semibold mb-4">Profiles</h1>
      <ul className="space-y-2">
        {profiles.map(p => <li key={p.id} className="p-2 bg-white rounded shadow">{p.student_id || p.full_name || p.id}</li>)}
      </ul>
    </div>
  )
}
