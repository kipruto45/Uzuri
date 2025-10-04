import axiosClient from "../api/axiosClient";
export const fetchFees = () => axiosClient.get("/fees/").then((r) => r.data);
export const fetchFeeStatement = () =>
  axiosClient.get("/fees/statement/").then((r) => r.data);
