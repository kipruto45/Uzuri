import React, { useState } from 'react'

export default function MetadataEditor({ open, initial = {}, onClose, onSave }) {
  const [title, setTitle] = useState(initial.title || '')
  const [department, setDepartment] = useState(initial.department || '')
  const [altText, setAltText] = useState(initial.alt_text || '')

  if (!open) return null

  async function submit(e) {
    e.preventDefault()
    await onSave({ title, department, alt_text: altText })
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <form onSubmit={submit} className="bg-white rounded p-4 w-full max-w-md">
        <h3 className="font-medium mb-2">Edit metadata</h3>
        <label className="block mb-2">
          <div className="text-sm">Title</div>
          <input value={title} onChange={(e) => setTitle(e.target.value)} className="w-full border rounded px-2 py-1" />
        </label>
        <label className="block mb-2">
          <div className="text-sm">Department</div>
          <input value={department} onChange={(e) => setDepartment(e.target.value)} className="w-full border rounded px-2 py-1" />
        </label>
        <label className="block mb-4">
          <div className="text-sm">Alt text</div>
          <input value={altText} onChange={(e) => setAltText(e.target.value)} className="w-full border rounded px-2 py-1" />
        </label>
        <div className="flex justify-end gap-2">
          <button type="button" onClick={onClose} className="px-3 py-2 border rounded">Cancel</button>
          <button type="submit" className="px-3 py-2 bg-blue-600 text-white rounded">Save</button>
        </div>
      </form>
    </div>
  )
}
