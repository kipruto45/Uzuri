import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import axiosClient from '../api/axiosClient'

export const fetchPaymentsSummary = () => axiosClient.get('/payments/summary/').then((r) => r.data)

export function usePaymentsSummary() {
  return useQuery(['payments', 'summary'], fetchPaymentsSummary, { staleTime: 1000 * 30, retry: 1 })
}

export function useCreatePayment() {
  const qc = useQueryClient()
  return useMutation((payload) => axiosClient.post('/payments/', payload).then((r) => r.data), {
    onSuccess: () => qc.invalidateQueries(['payments', 'summary']),
  })
}
