import axiosClient from "../../api/axiosClient";

export const registerUnits = (payload) =>
  axiosClient.post("unit_registration/register/", payload);
export const getRegistrationStatus = () =>
  axiosClient.get("unit_registration/status/");
