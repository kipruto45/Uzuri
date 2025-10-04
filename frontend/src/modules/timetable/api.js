import axiosClient from "../../api/axiosClient";

export const fetchTimetable = () => axiosClient.get("timetable/");
