import axiosClient from '../api/axiosClient'

export const fetchStudentDashboard = () =>
  axiosClient.get('/dashboard/student/').then((r) => r.data)

export const fetchDashboardSummary = () =>
  axiosClient.get('/dashboard/summary/').then((r) => r.data)
