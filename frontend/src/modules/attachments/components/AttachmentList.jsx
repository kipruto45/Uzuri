import React from 'react'
import { useQuery } from '@tanstack/react-query'
import { listAttachments } from '../api'
import { downloadFromUrl } from '../../../utils/download'

export default function AttachmentList() {
  const { data, isLoading } = useQuery(['attachments'], listAttachments)

  if (isLoading) return <div className="p-4">Loading attachments...</div>

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 p-4">
      {data.results?.map((a) => (
        <div key={a.id} className="bg-white rounded-lg shadow-sm overflow-hidden">
          {a.thumbnail_url ? (
            <img src={a.thumbnail_url} alt={a.name} className="w-full h-40 object-cover" />
          ) : (
            <div className="w-full h-40 bg-gray-100 flex items-center justify-center">No image</div>
          )}
          <div className="p-3 flex items-center justify-between">
            <div className="text-sm font-medium truncate" title={a.name}>{a.name}</div>
            <button className="text-sm text-blue-600 hover:underline" onClick={() => downloadFromUrl(a.file_url)}>Download</button>
          </div>
        </div>
      ))}
    </div>
  )
}
