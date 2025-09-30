import React from 'react'
import Dialog, { DialogOverlay, DialogTitle } from '../../../components/ui/Dialog'

export default function CombinedUploadModal({ open, onClose, progress, etaSeconds }) {
  const eta = etaSeconds == null ? null : `${Math.max(0, Math.round(etaSeconds))}s`
  return (
    <Dialog open={open} onClose={onClose} className="">
      <div className="min-h-screen px-4 text-center">
        <DialogOverlay className="fixed inset-0 bg-black opacity-40" />
        <span className="inline-block h-screen align-middle" aria-hidden>​</span>
        <div className="inline-block w-full max-w-md p-6 my-8 overflow-hidden align-middle bg-white dark:bg-gray-900 shadow-xl rounded-2xl">
          <DialogTitle className="text-lg font-medium">Uploading documents</DialogTitle>
          <div className="mt-4">
            <div className="text-sm text-gray-500 mb-2">Uploading attachments — please keep this window open until complete.</div>
            <div className="w-full h-3 bg-gray-100 rounded overflow-hidden">
              <div className="h-3 bg-indigo-600" style={{ width: `${progress}%` }} />
            </div>
            <div className="flex justify-between text-xs text-gray-500 mt-2">
              <div>{progress}%</div>
              <div>{eta ? `ETA: ${eta}` : ''}</div>
            </div>
          </div>
        </div>
      </div>
    </Dialog>
  )
}
