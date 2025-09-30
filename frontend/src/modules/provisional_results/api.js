import axiosClient from '../../api/axiosClient'

export const fetchProvisionalResults = () => axiosClient.get('provisional_results/')
