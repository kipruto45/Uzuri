import React from 'react'

export default function FileCard({ file, onDelete, onDownload }) {
  const sizeKB = file.size ? Math.round(file.size / 1024) : null
  return (
    <article className="bg-white rounded shadow-sm overflow-hidden" role="article" aria-labelledby={`file-${file.id}-name`}>
      <div className="w-full h-40 bg-gray-50 flex items-center justify-center">
        {file.thumbnail_url ? (
          <img src={file.thumbnail_url} alt={file.alt_text || file.name} className="object-contain h-full" />
        ) : (
          <div className="text-gray-400">{file.type || 'file'}</div>
        )}
      </div>
      <div className="p-3">
        <h3 id={`file-${file.id}-name`} className="text-sm font-medium truncate" title={file.name}>{file.name}</h3>
        <div className="text-xs text-gray-500">{sizeKB ? `${sizeKB} KB` : ''} • {new Date(file.created_at).toLocaleString()}</div>
        <div className="mt-2 flex gap-2">
          <button onClick={() => onDownload(file.id)} className="text-sm px-2 py-1 border rounded">Download</button>
          <button onClick={() => onDelete(file.id)} className="text-sm px-2 py-1 border rounded text-red-600">Delete</button>
        </div>
      </div>
    </article>
  )
}
