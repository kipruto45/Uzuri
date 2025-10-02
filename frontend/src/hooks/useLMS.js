import { useQuery } from '@tanstack/react-query'
import axiosClient from '../api/axiosClient'

export const fetchLMSCourses = () => axiosClient.get('/lms/courses/').then((r) => r.data)

export function useLMSCourses() {
  return useQuery(['lms', 'courses'], fetchLMSCourses, { staleTime: 1000 * 60, retry: 1 })
}
