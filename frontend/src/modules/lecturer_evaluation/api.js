import axiosClient from '../../api/axiosClient'

export const submitEvaluation = (payload) => axiosClient.post('lecturer_evaluation/submit/', payload)
export const fetchEvaluationStats = () => axiosClient.get('lecturer_evaluation/stats/')
