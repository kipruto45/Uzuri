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
