import React from 'react'
import { Plus } from 'lucide-react'

export default function FAB({ onClick }) {
  return (
    <button onClick={onClick} aria-label="New" className="fixed bottom-6 right-6 md:hidden bg-indigo-600 text-white p-4 rounded-full shadow-lg">
      <Plus className="w-5 h-5" />
    </button>
  )
}
