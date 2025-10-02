import React, { useEffect, useState } from 'react'
import { listRoles } from './api'

export default function RolesPage() {
  const [roles, setRoles] = useState([])
  useEffect(() => { let mounted = true; listRoles().then(r => { if (mounted) setRoles(r || []) }); return () => mounted = false }, [])
  return (
    <div className="p-6">
      <h1 className="text-xl font-semibold mb-4">Roles</h1>
      <ul className="space-y-2">
        {roles.map(r => <li key={r.id} className="p-2 bg-white rounded shadow">{r.name || r.id}</li>)}
      </ul>
    </div>
  )
}
