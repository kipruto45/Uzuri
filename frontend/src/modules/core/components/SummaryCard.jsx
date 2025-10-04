import React from "react";

export default function SummaryCard({ title, value, icon }) {
  return (
    <div className="bg-white p-4 rounded shadow flex items-center gap-4">
      <div className="p-2 bg-indigo-50 rounded">{icon}</div>
      <div>
        <div className="text-sm text-gray-500">{title}</div>
        <div className="text-2xl font-semibold">{value ?? "—"}</div>
      </div>
    </div>
  );
}
