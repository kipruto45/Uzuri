import React, { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { listLeaveRequests, createLeaveRequest } from '../api'

function NewLeaveForm({ onCreated }) {
  const [form, setForm] = useState({ leave_type: '', reason: '', start_date: '', end_date: '' })

  const mutation = useMutation(createLeaveRequest, {
    onSuccess: () => {
      onCreated()
    },
  })

  const submit = (e) => {
    e.preventDefault()
    mutation.mutate(form)
  }

  return (
    <form onSubmit={submit} className="new-leave-form">
      <label>
        Type
        <input value={form.leave_type} onChange={(e) => setForm({ ...form, leave_type: e.target.value })} />
      </label>
      <label>
        Start
        <input type="date" value={form.start_date} onChange={(e) => setForm({ ...form, start_date: e.target.value })} />
      </label>
      <label>
        End
        <input type="date" value={form.end_date} onChange={(e) => setForm({ ...form, end_date: e.target.value })} />
      </label>
      <label>
        Reason
        <textarea value={form.reason} onChange={(e) => setForm({ ...form, reason: e.target.value })} />
      </label>
      <button type="submit">Submit</button>
    </form>
  )
}

export default function LeaveListPage() {
  const queryClient = useQueryClient()
  const { data, isLoading } = useQuery(['leaveRequests'], () => listLeaveRequests({ page_size: 20 }))

  const onCreated = () => queryClient.invalidateQueries(['leaveRequests'])

  if (isLoading) return <div className="p-4">Loading...</div>

  return (
    <div className="p-4 max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-semibold">Academic Leave Requests</h2>
      </div>

      <div className="mb-6">
        <div className="bg-white p-4 rounded shadow-sm">
          <h3 className="text-lg font-medium mb-2">Submit a new leave request</h3>
          <NewLeaveForm onCreated={onCreated} />
        </div>
      </div>

      <div className="grid gap-4">
        {data.results?.map((l) => (
          <div key={l.id} className="bg-white rounded shadow p-4">
            <div className="flex items-center justify-between mb-2">
              <div className="text-sm font-medium">{l.leave_type}</div>
              <div className={`text-xs px-2 py-1 rounded ${l.status === 'approved' ? 'bg-green-100 text-green-800' : l.status === 'rejected' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'}`}>{l.status}</div>
            </div>
            <div className="text-sm text-gray-600 mb-2">{l.start_date} → {l.end_date}</div>
            <div className="text-sm">{l.reason}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
