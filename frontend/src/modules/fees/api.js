import axiosClient from '../../api/axiosClient'

export const fetchStatements = () => axiosClient.get('fees/statements/')
export const fetchReceipts = () => axiosClient.get('fees/receipts/')
