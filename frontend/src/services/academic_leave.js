import axiosClient from "../api/axiosClient";
// Backend routes are mounted under /academic-leave/ (see backend/core/urls.py)
export const listLeaveRequests = (params) =>
  axiosClient.get("/academic-leave/requests/", { params }).then((r) => r.data);
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
