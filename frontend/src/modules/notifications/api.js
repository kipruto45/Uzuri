import axiosClient from "../../api/axiosClient";

export const fetchNotifications = async () => {
  const res = await axiosClient.get("notifications/");
  return res.data;
};

export const markRead = async (id) => {
  const res = await axiosClient.post(`notifications/${id}/mark_read/`);
  return res.data;
};
