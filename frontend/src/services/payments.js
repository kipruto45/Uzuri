import axiosClient from '../api/axiosClient'
export const fetchPayments = () => axiosClient.get('/payments/').then(r=>r.data)
export const fetchReceipts = () => axiosClient.get('/payments/receipts/').then(r=>r.data)
