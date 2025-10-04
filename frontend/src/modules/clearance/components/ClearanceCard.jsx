import React from "react";
import { DocumentIcon, TrashIcon } from "./Icons";

export default function ClearanceCard({ doc, onDelete, onDownload }) {
  const sizeKB = doc.size ? Math.round(doc.size / 1024) : null;
  return (
    <article className="bg-white rounded-lg shadow-sm overflow-hidden flex flex-col">
      <div className="p-4 flex items-start gap-3">
        <div className="p-3 bg-blue-50 rounded">
          <DocumentIcon className="w-7 h-7 text-blue-600" />
        </div>
        <div className="flex-1">
          <h3 className="text-sm font-medium truncate" title={doc.title}>
            {doc.title}
          </h3>
          <p className="text-xs text-gray-500">
            {doc.department || "General"} • {doc.uploaded_by?.name || ""}
          </p>
          <p className="text-xs text-gray-400 mt-1">
            {sizeKB ? `${sizeKB} KB` : ""} •{" "}
            {new Date(doc.created_at).toLocaleDateString()}
          </p>
        </div>
      </div>
      <div className="p-2 bg-gray-50 flex items-center justify-end gap-2">
        <button
          onClick={() => onPreview(doc.id)}
          className="px-2 py-1 text-sm border rounded"
        >
          Preview
        </button>
        <button
          onClick={() => onDownload(doc.id)}
          className="px-2 py-1 text-sm border rounded"
        >
          Download
        </button>
        <button
          onClick={() => onEdit(doc)}
          className="px-2 py-1 text-sm border rounded"
        >
          Edit
        </button>
        <button
          onClick={() => onDelete(doc.id)}
          className="px-2 py-1 text-sm text-red-600 flex items-center gap-1"
        >
          <TrashIcon /> Delete
        </button>
      </div>
    </article>
  );
}
