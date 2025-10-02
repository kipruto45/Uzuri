import { useQuery } from '@tanstack/react-query'
import axiosClient from '../api/axiosClient'

export const fetchLearningPathways = () => axiosClient.get('/learning_pathways/').then((r) => r.data)

export function useLearningPathways() {
  return useQuery(['learning_pathways'], fetchLearningPathways, { staleTime: 1000 * 60, retry: 1 })
}
