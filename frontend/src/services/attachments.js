import axiosClient from "../api/axiosClient";
export const listAttachments = (params) =>
  axiosClient.get("/attachments/", { params }).then((r) => r.data);
export const uploadAttachment = (formData) =>
  axiosClient
    .post("/attachments/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    })
    .then((r) => r.data);
