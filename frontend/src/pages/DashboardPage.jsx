import React from 'react'
import { Card, CardContent } from '../components/ui/Card'
import { motion } from 'framer-motion'
import { User, Wallet, Home } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function DashboardPage() {
  const cards = [
    { title: 'My Profile', desc: 'View & update details', icon: <User className="w-8 h-8 text-blue-500" />, link: '/profile' },
    { title: 'Fees', desc: 'Check & pay fees', icon: <Wallet className="w-8 h-8 text-green-500" />, link: '/fees' },
    { title: 'Hostel', desc: 'Book your hostel room', icon: <Home className="w-8 h-8 text-yellow-500" />, link: '/hostel' },
  ]

  return (
    <div className="p-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {cards.map((c, i) => (
          <motion.div whileHover={{ scale: 1.03 }} key={i}>
            <Card>
              <CardContent className="flex items-center gap-4 p-6">
                {c.icon}
                <div>
                  <h2 className="text-xl font-bold">{c.title}</h2>
                  <p className="text-sm text-gray-500">{c.desc}</p>
                </div>
                <div className="ml-auto">
                  <Link to={c.link} className="text-sm text-blue-600">Open</Link>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>
    </div>
  )
}
