import axiosClient from "../../api/axiosClient";

// Routes are mounted under /academic-leave/ on the backend
export const listLeaveRequests = (params) =>
  axiosClient.get("/academic-leave/requests/", { params }).then((r) => r.data);
export const getLeaveRequest = (id) =>
  axiosClient.get(`/academic-leave/requests/${id}/`).then((r) => r.data);
export const createLeaveRequest = (payload) =>
  axiosClient.post("/academic-leave/requests/", payload).then((r) => r.data);
export const uploadLeaveDocument = (id, formData, onUploadProgress) =>
  axiosClient
    .post(`/academic-leave/requests/${id}/submit_document/`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
      onUploadProgress,
    })
    .then((r) => r.data);
export const approveLeave = (id, payload) =>
  axiosClient
    .post(`/academic-leave/requests/${id}/approve/`, payload)
    .then((r) => r.data);
export const rejectLeave = (id, payload) =>
  axiosClient
    .post(`/academic-leave/requests/${id}/reject/`, payload)
    .then((r) => r.data);

// legacy helpers (kept for backward compatibility)
export const applyLeave = createLeaveRequest;
export const fetchLeaveStatus = (params) =>
  axiosClient.get("academic_leave/status/", { params }).then((r) => r.data);
