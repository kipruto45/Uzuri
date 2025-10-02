import React from 'react'
import * as RadixDialog from '@radix-ui/react-dialog'

// Radix-based Dialog wrapper that provides the previous API surface used across the app.
export default function Dialog({ open, onClose, children, className, initialFocus }) {
  return (
    <RadixDialog.Root open={open} onOpenChange={(o) => { if (!o) onClose && onClose() }}>
      <RadixDialog.Portal>
        <div className={`fixed inset-0 z-50 ${className || ''}`}>
          {children}
        </div>
      </RadixDialog.Portal>
    </RadixDialog.Root>
  )
}

export const DialogOverlay = ({ className }) => (
  <RadixDialog.Overlay className={className} />
)

export const DialogTitle = ({ children, className }) => (
  <RadixDialog.Title className={className}>{children}</RadixDialog.Title>
)
