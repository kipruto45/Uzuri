import React from 'react'
import { Card, CardContent } from './ui/Card'
import { Bell } from 'lucide-react'
import { Link } from 'react-router-dom'
import { useNotifications, useMarkRead } from '../hooks/useNotifications'
import toast from 'react-hot-toast'

export default function NotificationsWidget() {
  const { data, isLoading, isError, refetch } = useNotifications(5)
  const markRead = useMarkRead()

  if (isLoading) return <div className="animate-pulse bg-white border rounded p-4 h-32" />

  if (isError) return (
    <div className="bg-white border rounded p-4">
      <div className="flex items-center justify-between">
        <h3 className="font-semibold flex items-center gap-2"><Bell className="w-4 h-4 text-blue-500" />Notifications</h3>
        <Link to="/notifications" className="text-xs text-gray-500">View all</Link>
      </div>
      <div className="text-sm text-red-600 mt-2">Unable to load notifications <button onClick={() => refetch()} className="ml-2 text-blue-600">Retry</button></div>
    </div>
  )

  return (
    <Card>
      <CardContent>
        <div className="flex items-center justify-between">
          <h3 className="font-semibold flex items-center gap-2"><Bell className="w-4 h-4 text-blue-500" />Notifications</h3>
          <Link to="/notifications" className="text-xs text-gray-500">View all</Link>
        </div>
        <ul className="mt-2 space-y-2">
          {(!data || data.length === 0) ? (
            <li className="text-sm text-gray-500">No notifications</li>
          ) : data.map((n) => (
            <li key={n.id} className="flex items-start justify-between">
              <div>
                <div className={`text-sm font-medium ${n.is_read ? 'text-gray-500' : 'text-black'}`}>{n.title}</div>
                <div className="text-xs text-gray-500">{n.created_at ? new Date(n.created_at).toLocaleString() : ''}</div>
              </div>
              <div className="ml-4">
                {!n.is_read && <button onClick={() => {
                  markRead.mutate(n.id, {
                    onSuccess: () => toast.success('Marked read'),
                    onError: () => toast.error('Failed to mark read')
                  })
                }} className="text-xs text-blue-600">Mark read</button>}
              </div>
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  )
}
