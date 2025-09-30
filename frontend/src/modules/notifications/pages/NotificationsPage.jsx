import React from 'react'
import { useSelector } from 'react-redux'

export default function NotificationsPage(){
  const items = useSelector(s => s.notifications.items)

  return (
    <div>
      <h2>Notifications</h2>
      <ul>
        {items.length === 0 && <li>No notifications yet</li>}
        {items.map((n, i) => (
          <li key={i}>{n.message || JSON.stringify(n)}</li>
        ))}
      </ul>
    </div>
  )
}
