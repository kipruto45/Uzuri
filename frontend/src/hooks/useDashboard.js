import { useQuery } from '@tanstack/react-query'
import { fetchStudentDashboard, fetchDashboardSummary } from '../services/dashboard'

export function useStudentDashboard() {
  return useQuery(['dashboard', 'student'], fetchStudentDashboard, { staleTime: 1000 * 60 })
}

export function useDashboardSummary() {
  return useQuery(['dashboard', 'summary'], fetchDashboardSummary, { staleTime: 1000 * 60 })
}
