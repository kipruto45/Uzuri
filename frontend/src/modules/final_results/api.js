import axiosClient from '../../api/axiosClient'

export const fetchFinalResults = () => axiosClient.get('final_results/')
