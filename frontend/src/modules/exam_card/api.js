import axiosClient from '../../api/axiosClient'

export const fetchExamCards = () => axiosClient.get('exam_card/')
export const downloadExamCard = (id) => axiosClient.get(`exam_card/${id}/download/`, { responseType: 'blob' })
