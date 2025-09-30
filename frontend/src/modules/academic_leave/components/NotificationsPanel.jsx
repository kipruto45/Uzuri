import React from 'react'
import { CheckCircle, XCircle, Info, Bell, Paperclip } from 'lucide-react'
import { motion } from 'framer-motion'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { fetchNotifications, markNotificationRead } from '../notifications'
import axiosClient from '../../api/axiosClient'

const iconMap = {
  approved: <CheckCircle className="w-5 h-5 text-green-500" />,
  rejected: <XCircle className="w-5 h-5 text-red-500" />,
  info: <Info className="w-5 h-5 text-blue-500" />,
  uploaded: <Paperclip className="w-5 h-5 text-indigo-500" />,
}

export default function NotificationsPanel() {
  const qc = useQueryClient()
  const { data, isLoading } = useQuery(['notifications'], () => fetchNotifications({ page_size: 10 }))

  const mutation = useMutation(markNotificationRead, {
    onSuccess: () => qc.invalidateQueries(['notifications'])
  })

  const markAll = async () => {
    if (!data?.results?.length) return
    try {
      await Promise.all(data.results.map(n => axiosClient.post(`/notifications/${n.id}/mark_read/`)))
      qc.invalidateQueries(['notifications'])
    } catch (e) {
      // ignore
    }
  }

  if (isLoading) return <div className="space-y-2">
    {[1,2].map(i => <div key={i} className="h-12 bg-gray-100 dark:bg-gray-800 rounded animate-pulse" />)}
  </div>

  if (!data?.results?.length) return <div className="text-sm text-gray-500">No notifications</div>

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <div className="text-sm font-medium">Recent</div>
        <div>
          <button onClick={markAll} className="text-xs text-indigo-600">Mark all read</button>
        </div>
      </div>

      {data.results.map((n) => (
        <motion.div key={n.id} initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} className={`p-3 rounded-md bg-white dark:bg-gray-800 border`}> 
          <div className="flex items-start justify-between">
            <div className="flex items-start space-x-3">
              <div>{iconMap[n.type] || <Bell className="w-5 h-5" />}</div>
              <div>
                <div className="text-sm font-medium">{n.title}</div>
                <div className="text-xs text-gray-500">{n.message}</div>
                <div className="text-xs text-gray-400 mt-1">{new Date(n.created_at).toLocaleString()}</div>
              </div>
            </div>

            <div>
              <button onClick={() => mutation.mutate(n.id)} className="text-xs text-indigo-600">Mark as read</button>
            </div>
          </div>
        </motion.div>
      ))}
    </div>
  )
}
