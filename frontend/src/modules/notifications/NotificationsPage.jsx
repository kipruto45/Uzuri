import React, { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { loadNotifications } from './notificationsSlice'
import NotificationList from './components/NotificationList'

export default function NotificationsPage() {
  const dispatch = useDispatch()
  const items = useSelector((s) => s.notifications.items)

  useEffect(() => {
    dispatch(loadNotifications())
  }, [dispatch])

  return (
    <div className="p-4">
      <h2 className="text-xl mb-2">Notifications</h2>
      <NotificationList items={items} />
    </div>
  )
}
