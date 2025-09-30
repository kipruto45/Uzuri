import axiosClient from '../../api/axiosClient'

export const fetchProfile = async () => {
  const res = await axiosClient.get('my_profile/me/')
  return res.data
}

export const updateProfile = async (payload) => {
  const res = await axiosClient.put('my_profile/me/', payload)
  return res.data
}
