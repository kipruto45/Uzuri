import axiosClient from '../api/axiosClient'
export const listNotifications = () => axiosClient.get('/notifications/').then(r=>r.data)
export const markRead = (id) => axiosClient.post(`/notifications/${id}/mark_read/`).then(r=>r.data)
