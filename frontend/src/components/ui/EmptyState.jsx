import React from "react";

export default function EmptyState({ title, message, action }) {
  return (
    <div className="p-8 bg-white rounded shadow text-center">
      <div className="text-xl font-semibold">{title}</div>
      {message && <div className="text-sm text-gray-500 mt-2">{message}</div>}
      {action && <div className="mt-4">{action}</div>}
    </div>
  );
}
