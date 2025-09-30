import axiosClient from '../../api/axiosClient'

export const listAttachments = async () => {
  const res = await axiosClient.get('attachments/')
  return res.data
}

export const uploadAttachment = async (formData) => {
  const res = await axiosClient.post('attachments/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return res.data
}
