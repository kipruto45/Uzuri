import React, { useEffect, useState } from 'react'
import { getClearanceVersions, getClearanceAuditLogs } from '../api'

export default function VersionsModal({ open, id, onClose }) {
  const [versions, setVersions] = useState([])
  const [logs, setLogs] = useState([])

  useEffect(() => {
    if (!open || !id) return
    let mounted = true
    async function load() {
      const v = await getClearanceVersions(id)
      const l = await getClearanceAuditLogs(id)
      if (mounted) {
        setVersions(v)
        setLogs(l)
      }
    }
    load()
    return () => (mounted = false)
  }, [open, id])

  if (!open) return null
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded p-4 w-full max-w-2xl max-h-[80vh] overflow-auto">
        <div className="flex justify-between items-center mb-3">
          <h3 className="font-medium">Versions & Audit</h3>
          <button onClick={onClose} className="px-2 py-1 border rounded">Close</button>
        </div>
        <section className="mb-4">
          <h4 className="text-sm font-semibold">Versions</h4>
          {versions.length === 0 ? <div className="text-sm text-gray-500">No versions available</div> : (
            <ul className="mt-2 space-y-2">
              {versions.map((v) => (
                <li key={v.id} className="text-sm">
                  <strong>{v.version}</strong> — {new Date(v.created_at).toLocaleString()} — {v.note || ''}
                </li>
              ))}
            </ul>
          )}
        </section>
        <section>
          <h4 className="text-sm font-semibold">Audit Logs</h4>
          {logs.length === 0 ? <div className="text-sm text-gray-500">No audit logs</div> : (
            <ul className="mt-2 space-y-2 text-sm">
              {logs.map((l) => (
                <li key={l.id}>{new Date(l.timestamp).toLocaleString()} — {l.user?.name || l.user} — {l.action} {JSON.stringify(l.details || '')}</li>
              ))}
            </ul>
          )}
        </section>
      </div>
    </div>
  )
}
