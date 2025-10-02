import React, { useState } from 'react'

export default function MetadataEditor({ open, initial = {}, onClose, onSave }) {
  const [title, setTitle] = useState(initial.title || '')
  const [department, setDepartment] = useState(initial.department || '')
  const [altText, setAltText] = useState(initial.alt_text || '')
  const [errors, setErrors] = useState({})

  if (!open) return null

  function validate() {
    const e = {}
    if (!title || title.trim().length < 3) e.title = 'Title is required (min 3 chars)'
    if (department && department.length > 100) e.department = 'Department too long'
    if (altText && altText.length > 250) e.altText = 'Alt text too long'
    return e
  }

  async function submit(e) {
    e.preventDefault()
    const eout = validate()
    setErrors(eout)
    if (Object.keys(eout).length > 0) return
    await onSave({ title, department, alt_text: altText })
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <form onSubmit={submit} className="bg-white rounded p-4 w-full max-w-md">
        <h3 className="font-medium mb-2">Edit metadata</h3>
        <label className="block mb-2">
          <div className="text-sm">Title</div>
          <input value={title} onChange={(e) => setTitle(e.target.value)} className="w-full border rounded px-2 py-1" />
          {errors.title && <div className="text-xs text-red-600 mt-1">{errors.title}</div>}
        </label>
        <label className="block mb-2">
          <div className="text-sm">Department</div>
          <input value={department} onChange={(e) => setDepartment(e.target.value)} className="w-full border rounded px-2 py-1" />
          {errors.department && <div className="text-xs text-red-600 mt-1">{errors.department}</div>}
        </label>
        <label className="block mb-4">
          <div className="text-sm">Alt text</div>
          <input value={altText} onChange={(e) => setAltText(e.target.value)} className="w-full border rounded px-2 py-1" />
          {errors.altText && <div className="text-xs text-red-600 mt-1">{errors.altText}</div>}
        </label>
        <div className="flex justify-end gap-2">
          <button type="button" onClick={onClose} className="px-3 py-2 border rounded">Cancel</button>
          <button type="submit" className="px-3 py-2 bg-blue-600 text-white rounded">Save</button>
        </div>
      </form>
    </div>
  )
}
