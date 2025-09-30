import axiosClient from '../../api/axiosClient'

export const fetchCases = () => axiosClient.get('disciplinary/')
export const submitAppeal = (id, payload) => axiosClient.post(`disciplinary/${id}/appeal/`, payload)
