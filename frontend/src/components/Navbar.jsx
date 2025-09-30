import React from 'react'
import { Bell } from 'lucide-react'
import DarkModeToggle from './DarkModeToggle'

export default function Navbar({ onToggle }) {
  return (
    <header className="w-full flex items-center justify-between p-4 bg-white dark:bg-gray-900 shadow-sm">
      <div className="flex items-center gap-4">
        <button className="md:hidden" onClick={onToggle} aria-label="Open menu">☰</button>
        <h1 className="text-lg font-bold">Uzuri</h1>
      </div>
      <div className="flex items-center gap-3">
        <DarkModeToggle />
        <button className="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800"><Bell /></button>
        <div className="w-8 h-8 rounded-full bg-gray-200 dark:bg-gray-700" />
      </div>
    </header>
  )
}
