import axios from 'axios'

const BASE = '/api/attachments/'

export async function listAttachments() {
  const res = await axios.get(BASE)
  return res.data
}

export async function uploadAttachment(formData) {
  const res = await axios.post(BASE, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return res.data
}

export async function deleteAttachment(id) {
  const res = await axios.delete(`${BASE}${id}/`)
  return res.data
}

export async function downloadAttachmentUrl(id) {
  // returns a URL to download the file (backend should provide)
  const res = await axios.get(`${BASE}${id}/download/`)
  return res.data
}

export async function getAttachmentVersions(id) {
  const res = await axios.get(`${BASE}${id}/versions/`)
  return res.data
}
