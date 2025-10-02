import axiosClient from '../../api/axiosClient'

export async function fetchCoreOverview() {
  // fetch counts for key resources
  const endpoints = [
    'core/roles/',
    'core/users/',
    'core/profiles/',
    'core/system-metrics/',
    'core/audit-logs/?page_size=5',
  ]
  try {
    const [roles, users, profiles, metrics, logs] = await Promise.all(endpoints.map((p) => axiosClient.get(p).then((r) => r.data).catch(() => null)))
    return { roles, users, profiles, metrics, logs }
  } catch (e) {
    console.error('overview fetch failed', e)
    return { roles: null, users: null, profiles: null, metrics: null, logs: null }
  }
}

export async function fetchAuditLogs(params = {}) {
  const res = await axiosClient.get('core/audit-logs/', { params })
  return res.data
}

export async function listRoles(params = {}) {
  const res = await axiosClient.get('core/roles/', { params })
  return res.data
}

export async function listUsers(params = {}) {
  const res = await axiosClient.get('core/users/', { params })
  return res.data
}

export async function listProfiles(params = {}) {
  const res = await axiosClient.get('core/profiles/', { params })
  return res.data
}

// Generic list wrappers for other core router-registered resources
export async function listPrograms(params = {}) { const res = await axiosClient.get('core/programs/', { params }); return res.data }
export async function listCourses(params = {}) { const res = await axiosClient.get('core/courses/', { params }); return res.data }
export async function listUnits(params = {}) { const res = await axiosClient.get('core/units/', { params }); return res.data }
export async function listRegistrations(params = {}) { const res = await axiosClient.get('core/registrations/', { params }); return res.data }
export async function listTranscripts(params = {}) { const res = await axiosClient.get('core/transcripts/', { params }); return res.data }
export async function listGrades(params = {}) { const res = await axiosClient.get('core/grades/', { params }); return res.data }
export async function listAssignments(params = {}) { const res = await axiosClient.get('core/assignments/', { params }); return res.data }
export async function listSubmissions(params = {}) { const res = await axiosClient.get('core/submissions/', { params }); return res.data }
export async function listInvoices(params = {}) { const res = await axiosClient.get('core/invoices/', { params }); return res.data }
export async function listTransactions(params = {}) { const res = await axiosClient.get('core/transactions/', { params }); return res.data }
export async function listReceipts(params = {}) { const res = await axiosClient.get('core/receipts/', { params }); return res.data }
export async function listScholarships(params = {}) { const res = await axiosClient.get('core/scholarships/', { params }); return res.data }
export async function listHostelApplications(params = {}) { const res = await axiosClient.get('core/hostel-applications/', { params }); return res.data }
export async function listLeaveRequests(params = {}) { const res = await axiosClient.get('core/leave-requests/', { params }); return res.data }
export async function listMessages(params = {}) { const res = await axiosClient.get('core/messages/', { params }); return res.data }
export async function listTickets(params = {}) { const res = await axiosClient.get('core/tickets/', { params }); return res.data }
export async function listAdminActionLogs(params = {}) { const res = await axiosClient.get('core/admin-action-logs/', { params }); return res.data }
export async function getSystemMetrics(params = {}) { const res = await axiosClient.get('core/system-metrics/', { params }); return res.data }
