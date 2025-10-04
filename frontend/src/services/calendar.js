import axiosClient from "../api/axiosClient";

export const listCalendarEvents = () =>
  axiosClient.get("/calendar/events/").then((r) => r.data);
