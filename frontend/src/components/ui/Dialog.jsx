import React from 'react'
import * as RadixDialog from '@radix-ui/react-dialog'

// A small wrapper that exposes a similar surface to previous Dialog usage.
export default function Dialog({ open, onClose, children, className }) {
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
