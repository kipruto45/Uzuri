import React, { useEffect, useState } from 'react'
import { listAttachments, uploadAttachment } from './api'

export default function AttachmentsPage() {
  const [items, setItems] = useState([])

  useEffect(() => {
    ;(async () => {
      const data = await listAttachments()
      setItems(data || [])
    })()
  }, [])

  const onUpload = async (e) => {
    const file = e.target.files[0]
    const fd = new FormData()
    fd.append('file', file)
    await uploadAttachment(fd)
    const data = await listAttachments()
    setItems(data || [])
  }

  return (
    <div className="p-4">
      <h2>Attachments</h2>
      <input type="file" onChange={onUpload} />
      <ul>
        {items.map((a) => (
          <li key={a.id}>{a.title || a.file}</li>
        ))}
      </ul>
    </div>
  )
}
