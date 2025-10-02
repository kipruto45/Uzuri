import React, { useEffect, useState } from 'react'
import { listUsers } from './api'

export default function UsersPage() {
  const [users, setUsers] = useState([])
  useEffect(() => { let mounted = true; listUsers().then(r => { if (mounted) setUsers(r || []) }); return () => mounted = false }, [])
  return (
    <div className="p-6">
      <h1 className="text-xl font-semibold mb-4">Users</h1>
      <ul className="space-y-2">
        {users.map(u => <li key={u.id} className="p-2 bg-white rounded shadow">{u.username || u.email || u.id}</li>)}
      </ul>
    </div>
  )
}
