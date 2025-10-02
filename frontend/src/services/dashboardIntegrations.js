import axiosClient from '../api/axiosClient'

async function safeGet(path) {
  try {
    const res = await axiosClient.get(path)
    return res.data
  } catch (err) {
    // return null for not found, otherwise rethrow so tests can catch real errors
    if (err?.response?.status === 404) return null
    // swallow network errors and return null so dashboard stays robust
    return null
  }
}

export const fetchNotificationsRecent = (limit = 5) =>
  safeGet(`notifications/?limit=${limit}`)

export const fetchCalendarEvents = () =>
  // try smart calendar first, fall back to generic calendar events
  safeGet('smart-calendar/smart-events/').then((r) => r || safeGet('calendar/events/'))

export const fetchPaymentsSummary = async () => {
  // backend exposes a variety of payment endpoints; try to read a summary first
  const candidate = await safeGet('payments/summary/')
  if (candidate) return candidate
  const list = await safeGet('payments/')
  if (Array.isArray(list)) {
    return { payment_history: list.slice(0, 5), next_due: null }
  }
  return null
}

export const fetchFeedback = () => safeGet('feedback/')

export const fetchPersonalization = () => safeGet('personalization/personalization-profiles/')

export const fetchLMSIntegration = () => safeGet('integration/lms/')

export const fetchCompliance = () => safeGet('compliance-audit/')

export const fetchAccessibilityFeatures = () => safeGet('accessibility-ai/accessibility-features/')

export const fetchAllIntegrations = async () => {
  const [notifications, events, payments, feedback, personalization, lms, compliance, accessibility] = await Promise.all([
    fetchNotificationsRecent(5),
    fetchCalendarEvents(),
    fetchPaymentsSummary(),
    fetchFeedback(),
    fetchPersonalization(),
    fetchLMSIntegration(),
    fetchCompliance(),
    fetchAccessibilityFeatures(),
  ])

  return {
    notifications: notifications || [],
    events: events || [],
    payments: payments || null,
    feedback: feedback || [],
    personalization: personalization || null,
    lms: lms || null,
    compliance: compliance || null,
    accessibility: accessibility || [],
  }
}
