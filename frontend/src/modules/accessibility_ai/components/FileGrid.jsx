import React from "react";
import FileCard from "./FileCard";

export default function FileGrid({ files = [], onDelete, onDownload }) {
  if (!files || files.length === 0) {
    return (
      <div className="p-6 text-center text-gray-500">No attachments yet</div>
    );
  }

  return (
    <div aria-live="polite">
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {files.map((f) => (
          <FileCard
            key={f.id}
            file={f}
            onDelete={onDelete}
            onDownload={onDownload}
          />
        ))}
      </div>
    </div>
  );
}
