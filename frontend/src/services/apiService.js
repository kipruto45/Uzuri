import api, { resolveApiUrl } from "../api/client";

// Use VITE_API_BASE if set (example: http://localhost:8000/api/v1)
const envBase = import.meta.env.VITE_API_BASE || "";
// Ensure prefix starts with / and does not end with /
function normalizeBase(b) {
  if (!b) return "/api/v1";
  try {
    const u = new URL(b);
    return u.pathname.replace(/\/$/, "") || "/";
  } catch {
    // b may be a path like /api or /api/v1
    return b.replace(/\/$/, "");
  }
}

const prefix = normalizeBase(envBase);

export const auth = {
  login: (payload) => api.post(`${prefix}/auth/login/`, payload),
  refresh: (payload) => api.post(`${prefix}/auth/refresh/`, payload),
  me: () => api.get(`${prefix}/auth/me/`),
};

export const attachments = {
  list: (params) => api.get(`${prefix}/attachments/`, { params }),
  upload: (formData) =>
    api.post(`${prefix}/attachments/`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    }),
};

export const notifications = {
  list: (params) => api.get(`${prefix}/notifications/`, { params }),
};

export const payments = {
  mpesa: (payload) => api.post(`${prefix}/payments/mpesa/`, payload),
  stripe: (payload) => api.post(`${prefix}/payments/stripe/`, payload),
  status: (id) => api.get(`${prefix}/payments/${id}/status/`),
};

export default {
  auth,
  attachments,
  notifications,
  payments,
};
