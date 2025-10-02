import React from 'react'

export default function PreviewModal({ open, fileBlob, fileName, onClose }) {
  if (!open) return null
  const url = fileBlob ? URL.createObjectURL(fileBlob) : null
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded shadow-lg max-w-4xl w-full max-h-[90vh] overflow-auto p-4">
        <div className="flex justify-between items-center mb-2">
          <h3 className="font-medium">Preview — {fileName}</h3>
          <button onClick={onClose} className="px-2 py-1 border rounded">Close</button>
        </div>
        <div className="h-[70vh]">
          {fileName && fileName.toLowerCase().endsWith('.pdf') ? (
            <iframe title="pdf-preview" src={url} className="w-full h-full" />
          ) : (
            <img src={url} alt={fileName} className="max-h-full mx-auto" />
          )}
        </div>
      </div>
    </div>
  )
}
