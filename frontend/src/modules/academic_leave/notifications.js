import axiosClient from '../../api/axiosClient'

export const fetchNotifications = (params) => axiosClient.get('/notifications/', { params }).then(r => r.data)
export const markNotificationRead = (id) => axiosClient.post(`/notifications/${id}/mark_read/`).then(r => r.data)
