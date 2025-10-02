import axiosClient from '../api/axiosClient'

export const listNotifications = (params) =>
  axiosClient.get('/notifications/', { params }).then((r) => r.data)

export const listUnreadCount = () => axiosClient.get('/notifications/unread_count/').then((r) => r.data)

export const markRead = (id) => axiosClient.post(`/notifications/${id}/mark_read/`).then((r) => r.data)
