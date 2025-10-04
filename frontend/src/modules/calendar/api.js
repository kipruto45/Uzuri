import axiosClient from "../../api/axiosClient";

const BASE = "calendar/events/";

export async function listEvents(params = {}) {
  const res = await axiosClient.get(BASE, { params });
  return res.data;
}

export async function myEvents() {
  const res = await axiosClient.get("calendar/events/my_events/");
  return res.data;
}

export async function createEvent(payload) {
  const res = await axiosClient.post(BASE, payload);
  return res.data;
}

export async function updateEvent(id, payload) {
  const res = await axiosClient.put(`calendar/events/${id}/`, payload);
  return res.data;
}

export async function deleteEvent(id) {
  const res = await axiosClient.delete(`calendar/events/${id}/`);
  return res.data;
}

export async function exportIcal() {
  const res = await axiosClient.get("calendar/events/ical-feed/", {
    responseType: "blob",
  });
  return res.data;
}

export async function googleAuthUrl() {
  const res = await axiosClient.get("calendar/events/google-auth-url/");
  return res.data;
}

export async function pushGoogle() {
  const res = await axiosClient.post("calendar/events/push-google/");
  return res.data;
}

export async function pullGoogle() {
  const res = await axiosClient.get("calendar/events/pull-google/");
  return res.data;
}
