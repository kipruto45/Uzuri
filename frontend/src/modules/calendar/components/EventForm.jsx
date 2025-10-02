import React, { useState } from 'react'

export default function EventForm({ initial = null, onSave, onCancel }) {
  const [title, setTitle] = useState(initial?.title || '')
  const [start, setStart] = useState(initial?.start_time || '')
  const [end, setEnd] = useState(initial?.end_time || '')
  const [location, setLocation] = useState(initial?.location || '')

  async function submit(e) {
    e.preventDefault()
    const payload = { title, start_time: start, end_time: end, location }
    await onSave(payload)
  }

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <form onSubmit={submit} className="bg-white p-6 rounded shadow-md w-full max-w-md" aria-label="Event form">
        <h2 className="text-lg font-semibold mb-2">{initial ? 'Edit Event' : 'New Event'}</h2>
        <label className="block mb-2">
          <div className="text-sm">Title</div>
          <input value={title} onChange={(e) => setTitle(e.target.value)} className="w-full border rounded px-2 py-1" required />
        </label>
        <label className="block mb-2">
          <div className="text-sm">Start</div>
          <input value={start} onChange={(e) => setStart(e.target.value)} type="datetime-local" className="w-full border rounded px-2 py-1" required />
        </label>
        <label className="block mb-2">
          <div className="text-sm">End</div>
          <input value={end} onChange={(e) => setEnd(e.target.value)} type="datetime-local" className="w-full border rounded px-2 py-1" required />
        </label>
        <label className="block mb-4">
          <div className="text-sm">Location</div>
          <input value={location} onChange={(e) => setLocation(e.target.value)} className="w-full border rounded px-2 py-1" />
        </label>
        <div className="flex justify-end gap-2">
          <button type="button" onClick={onCancel} className="px-3 py-2 border rounded">Cancel</button>
          <button type="submit" className="px-3 py-2 bg-blue-600 text-white rounded">Save</button>
        </div>
      </form>
    </div>
  )
}
