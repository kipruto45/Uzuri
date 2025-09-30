import React from 'react'
import { Dialog } from '@headlessui/react'

export default function PreviewModal({ open, src, name, onClose }) {
  if (!open) return null
  const isImage = /\.(png|jpe?g|gif|svg)$/i.test(name)
  const isPdf = /\.pdf$/i.test(name)
  return (
    <Dialog open={open} onClose={onClose} className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="fixed inset-0 bg-black/40" />
      <div className="bg-white dark:bg-gray-900 rounded-lg p-4 max-w-3xl w-full z-10">
        <div className="flex justify-between items-center mb-2">
          <div className="font-medium">Preview: {name}</div>
          <button onClick={onClose} className="text-sm text-gray-500">Close</button>
        </div>
        <div className="h-96 overflow-auto">
          {isImage ? <img src={src} alt={name} className="mx-auto max-h-full" /> : isPdf ? <iframe title={name} src={src} className="w-full h-full" /> : <div className="p-8">Preview not supported</div>}
        </div>
      </div>
    </Dialog>
  )
}
