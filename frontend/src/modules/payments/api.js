import axiosClient from "../../api/axiosClient";

export const startMpesa = async (payload) => {
  const res = await axiosClient.post("payments/mpesa/", payload);
  return res.data;
};

export const startStripe = async (payload) => {
  const res = await axiosClient.post("payments/stripe/", payload);
  return res.data;
};

export const listTransactions = async () => {
  const res = await axiosClient.get("payments/transactions/");
  return res.data;
};
