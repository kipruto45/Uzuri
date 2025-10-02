import React from 'react'

export default function FileTable({ files = [], onDelete, onDownload }) {
  if (!files || files.length === 0) return <div className="p-4 text-gray-500">No attachments</div>

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full bg-white">
        <thead>
          <tr>
            <th className="text-left p-2">Name</th>
            <th className="text-left p-2">Type</th>
            <th className="text-left p-2">Preview</th>
            <th className="text-right p-2">Size</th>
            <th className="text-right p-2">Date</th>
            <th className="text-center p-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          {files.map((f) => (
            <tr key={f.id} className="border-t hover:bg-gray-50">
              <td className="p-2">{f.name}</td>
              <td className="p-2">{f.type}</td>
              <td className="p-2">
                {f.thumbnail_url ? <img src={f.thumbnail_url} alt={f.alt_text || f.name} className="h-12" /> : <span className="text-xs text-gray-500">{(f.preview || '').slice(0, 80)}</span>}
              </td>
              <td className="p-2 text-right">{f.size ? Math.round(f.size / 1024) + ' KB' : ''}</td>
              <td className="p-2 text-right">{new Date(f.created_at).toLocaleString()}</td>
              <td className="p-2 text-center">
                <div className="flex items-center justify-center gap-2">
                  <button onClick={() => onDownload(f.id)} className="px-2 py-1 border rounded">Download</button>
                  <button onClick={() => onDelete(f.id)} className="px-2 py-1 border rounded text-red-600">Delete</button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
