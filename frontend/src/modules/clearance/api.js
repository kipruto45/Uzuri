import axiosClient from "../../api/axiosClient";

const BASE = "clearance/";

export async function listClearanceDocuments(params = {}) {
  const res = await axiosClient.get(`${BASE}`, { params });
  return res.data;
}

export async function uploadClearanceDocument(formData) {
  const res = await axiosClient.post(`${BASE}`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
}

export async function deleteClearanceDocument(id) {
  const res = await axiosClient.delete(`${BASE}${id}/`);
  return res.data;
}

export async function getClearanceDocument(id) {
  const res = await axiosClient.get(`${BASE}${id}/`);
  return res.data;
}

export async function updateClearanceDocument(id, payload) {
  const res = await axiosClient.patch(`${BASE}${id}/`, payload);
  return res.data;
}

export async function downloadClearanceDocument(id) {
  // returns a blob for download
  const res = await axiosClient.get(`${BASE}${id}/download/`, {
    responseType: "blob",
  });
  return res.data;
}

export async function getClearanceVersions(id) {
  try {
    const res = await axiosClient.get(`${BASE}${id}/versions/`);
    return res.data;
  } catch (e) {
    // backend may not support versions; return empty
    return [];
  }
}

export async function getClearanceAuditLogs(id) {
  try {
    const res = await axiosClient.get(`${BASE}${id}/audit/`);
    return res.data;
  } catch (e) {
    return [];
  }
}
