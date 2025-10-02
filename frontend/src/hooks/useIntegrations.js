import { useQuery } from '@tanstack/react-query'
import { fetchAllIntegrations } from '../services/dashboardIntegrations'

export function useAllIntegrations() {
  return useQuery(['integrations', 'all'], fetchAllIntegrations, { staleTime: 1000 * 30, retry: 1 })
}
