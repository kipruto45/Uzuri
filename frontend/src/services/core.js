import axiosClient from '../api/axiosClient'

export const fetchDashboard = () => axiosClient.get('/').then(r => r.data)
export const fetchRoles = () => axiosClient.get('/core/roles/').then(r => r.data)
