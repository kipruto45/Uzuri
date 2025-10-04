import React from "react";

export default function ActivityFeed({ logs = [] }) {
  if (!logs || logs.length === 0)
    return <div className="p-4 text-gray-500">No recent activity</div>;
  return (
    <ul className="space-y-2">
      {logs.map((l) => (
        <li key={l.id} className="p-2 bg-white rounded shadow-sm">
          <div className="text-sm text-gray-700">
            {l.action} — {l.user?.name || l.user} —{" "}
            <span className="text-xs text-gray-400">
              {new Date(l.timestamp).toLocaleString()}
            </span>
          </div>
        </li>
      ))}
    </ul>
  );
}
