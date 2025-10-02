import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import LoginPage from '../auth/LoginPage'
import DashboardPage from '../pages/DashboardPage'
import NotificationsPage from '../modules/notifications/NotificationsPage'
import FeesPage from '../modules/fee_management/FeesPage'
import AttachmentsPage from '../modules/attachments/AttachmentsPage'
import PaymentsPage from '../modules/payments/PaymentsPage'
import ProfilePage from '../modules/my_profile/ProfilePage'
import LeaveListPage from '../modules/academic_leave/pages/LeaveListPage'
import AcademicLeavePage from '../modules/academic_leave/AcademicLeavePage'
import AccessibilityPage from '../modules/accessibility_ai/AccessibilityPage'
import AiSupportPage from '../modules/ai_support/AiSupportPage'
import CalendarPage from '../modules/calendar/CalendarPage'
import ClearancePage from '../modules/clearance/ClearancePage'
import CoreDashboard from '../modules/core/CoreDashboard'
import UsersPage from '../modules/core/UsersPage'
import RolesPage from '../modules/core/RolesPage'
import ProfilesPage from '../modules/core/ProfilesPage'
import ResourcePage from '../modules/core/ResourcePage'
import RequireAuth from '../auth/RequireAuth'

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
  <Route path="/notifications" element={<RequireAuth><NotificationsPage /></RequireAuth>} />
  <Route path="/" element={<RequireAuth><DashboardPage /></RequireAuth>} />
      <Route path="/fees" element={<RequireAuth><FeesPage /></RequireAuth>} />
      <Route path="/attachments" element={<RequireAuth><AttachmentsPage /></RequireAuth>} />
      <Route path="/payments" element={<RequireAuth><PaymentsPage /></RequireAuth>} />
      <Route path="/profile" element={<RequireAuth><ProfilePage /></RequireAuth>} />
  <Route path="/academic-leave" element={<RequireAuth><AcademicLeavePage /></RequireAuth>} />
  <Route path="/accessibility" element={<RequireAuth><AccessibilityPage /></RequireAuth>} />
  <Route path="/ai-support" element={<RequireAuth><AiSupportPage /></RequireAuth>} />
    <Route path="/calendar" element={<RequireAuth><CalendarPage /></RequireAuth>} />
  <Route path="/clearance" element={<RequireAuth><ClearancePage /></RequireAuth>} />
  <Route path="/core" element={<RequireAuth><CoreDashboard /></RequireAuth>} />
  <Route path="/core/users" element={<RequireAuth><UsersPage /></RequireAuth>} />
  <Route path="/core/roles" element={<RequireAuth><RolesPage /></RequireAuth>} />
  <Route path="/core/profiles" element={<RequireAuth><ProfilesPage /></RequireAuth>} />
  <Route path="/core/:resource" element={<RequireAuth><ResourcePage /></RequireAuth>} />
      <Route path="/" element={<Navigate to="/notifications" replace />} />
    </Routes>
  )
}
