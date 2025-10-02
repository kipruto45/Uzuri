import axiosClient from '../../api/axiosClient'

// Backend router registers accessibility-features under the accessibility_ai app.
export const listAccessibilityFeatures = async () => {
  const res = await axiosClient.get('/accessibility-ai/accessibility-features/')
  return res.data
}

export const toggleAccessibilityFeature = async (id, payload) => {
  const res = await axiosClient.patch(`/accessibility-ai/accessibility-features/${id}/`, payload)
  return res.data
}

export const createAccessibilityFeature = async (payload) => {
  const res = await axiosClient.post('/accessibility-ai/accessibility-features/', payload)
  return res.data
}

export const deleteAccessibilityFeature = async (id) => {
  const res = await axiosClient.delete(`/accessibility-ai/accessibility-features/${id}/`)
  return res.data
}
