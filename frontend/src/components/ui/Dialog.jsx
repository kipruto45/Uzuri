import React, { useEffect } from 'react'
import ReactDOM from 'react-dom'

// Minimal ShadCN-style Dialog wrapper (small surface compatible with existing usage)
export default function Dialog({ open, onClose, children, className, initialFocus }) {
  useEffect(() => {
    if (!open) return
    if (initialFocus && initialFocus.current) {
      try { initialFocus.current.focus() } catch (e) {}
    }
  }, [open, initialFocus])

  if (!open) return null

  return ReactDOM.createPortal(
    <div className={`fixed inset-0 z-50 ${className || ''}`}> 
      {children}
    </div>,
    document.body
  )
}

Dialog.Overlay = function DialogOverlay({ className }) {
  return <div className={className} />
}

Dialog.Title = function DialogTitle({ children, className }) {
  return <h2 className={className}>{children}</h2>
}
