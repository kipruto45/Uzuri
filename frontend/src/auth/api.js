import axiosClient from "../api/axiosClient";

export const login = async (credentials) => {
  const res = await axiosClient.post("auth/login/", credentials);
  return res.data;
};

export const refresh = async (token) => {
  const res = await axiosClient.post("auth/refresh/", { refresh: token });
  return res.data;
};

export const me = async () => {
  const res = await axiosClient.get("auth/me/");
  return res.data;
};
