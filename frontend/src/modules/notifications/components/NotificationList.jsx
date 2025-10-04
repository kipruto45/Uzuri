import React from "react";

export default function NotificationList({ items = [] }) {
  if (!items.length) return <div>No notifications</div>;
  return (
    <ul>
      {items.map((n) => (
        <li key={n.id} className={n.read ? "text-gray-500" : "font-medium"}>
          <div>{n.title}</div>
          <div className="text-sm text-gray-600">{n.body}</div>
        </li>
      ))}
    </ul>
  );
}
