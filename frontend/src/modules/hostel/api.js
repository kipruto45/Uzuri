import axiosClient from '../../api/axiosClient'

export const applyHostel = (payload) => axiosClient.post('hostel/apply/', payload)
export const listRooms = () => axiosClient.get('hostel/rooms/')
