import React from 'react'
import { Link } from 'react-router-dom'
import { Home, User, Book, CreditCard, FileText, Calendar } from 'lucide-react'

const items = [
  { to: '/', label: 'Dashboard', icon: <Home /> },
  { to: '/profile', label: 'Profile', icon: <User /> },
  { to: '/fees', label: 'Fees', icon: <CreditCard /> },
  { to: '/hostel', label: 'Hostel', icon: <Book /> },
  { to: '/attachments', label: 'Attachments', icon: <FileText /> },
  { to: '/timetable', label: 'Timetable', icon: <Calendar /> },
]

export default function Sidebar() {
  return (
    <aside className="hidden md:block w-64 bg-gradient-to-b from-white to-gray-50 border-r">
      <div className="p-4">
        <h3 className="font-bold text-xl">Uzuri</h3>
      </div>
      <nav className="p-2">
        {items.map((it) => (
          <Link key={it.to} to={it.to} className="flex items-center gap-3 p-3 rounded hover:bg-gray-100">
            <span className="w-6 h-6">{it.icon}</span>
            <span>{it.label}</span>
          </Link>
        ))}
      </nav>
    </aside>
  )
}
