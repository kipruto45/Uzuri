import axiosClient from "../../api/axiosClient";

export const fetchGraduationStatus = () =>
  axiosClient.get("graduation/status/");
