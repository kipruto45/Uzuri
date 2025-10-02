import React, { useState } from 'react'
import { Card, CardContent } from './ui/Card'
import { Upload } from 'lucide-react'
import axiosClient from '../api/axiosClient'

export default function AttachmentsUploader() {
  const [files, setFiles] = useState([])
  const [uploading, setUploading] = useState(false)

  const onFiles = (e) => {
    setFiles(Array.from(e.target.files))
  }

  const upload = async () => {
    if (files.length === 0) return
    setUploading(true)
    try {
      for (const f of files) {
        const fd = new FormData()
        fd.append('file', f)
        // basic POST - server should accept multipart/form-data
        await axiosClient.post('attachments/', fd)
      }
      setFiles([])
    } catch (e) {
      // ignore for now - add per-file error handling later
    } finally {
      setUploading(false)
    }
  }

  return (
    <Card>
      <CardContent>
        <div className="flex items-center justify-between">
          <h3 className="font-semibold flex items-center gap-2"><Upload className="w-4 h-4" />Attachments</h3>
        </div>
        <div className="mt-2">
          <input type="file" onChange={onFiles} multiple />
          <div className="mt-2">
            {files.length > 0 && <div className="text-sm text-gray-700">{files.length} file(s) selected</div>}
            <button onClick={upload} disabled={uploading || files.length === 0} className="mt-2 px-3 py-1 bg-blue-600 text-white rounded disabled:opacity-50">{uploading ? 'Uploading…' : 'Upload'}</button>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
