import React from 'react'
import { Card, CardContent } from './ui/Card'
import { User } from 'lucide-react'
import { Link } from 'react-router-dom'
import { useStudentDashboard } from '../hooks/useDashboard'

export default function ProfileCard() {
  const { data: student, isLoading } = useStudentDashboard()

  if (isLoading) return <div className="animate-pulse bg-white border rounded p-4 h-28" />

  const user = student?.user || { first_name: 'Student', last_name: '' }

  return (
    <Card>
      <CardContent className="flex items-center gap-4">
        <User className="w-12 h-12 text-blue-500" aria-hidden />
        <div>
          <div className="text-lg font-semibold">{user.first_name} {user.last_name}</div>
          <div className="text-sm text-gray-500">{student?.program || ''}</div>
          <div className="mt-2 flex gap-2">
            <Link to="/academic-leave" className="text-xs text-blue-600">Apply leave</Link>
            <Link to="/attachments" className="text-xs text-blue-600">Upload docs</Link>
            <Link to="/timetable" className="text-xs text-blue-600">View timetable</Link>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
