import React from "react";
import ClearanceCard from "./ClearanceCard";

export default function ClearanceList({ docs = [], onDelete, onDownload }) {
  if (!docs || docs.length === 0)
    return (
      <div className="p-6 text-gray-500">No clearance documents found</div>
    );

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      {docs.map((d) => (
        <ClearanceCard
          key={d.id}
          doc={d}
          onDelete={onDelete}
          onDownload={onDownload}
        />
      ))}
    </div>
  );
}
