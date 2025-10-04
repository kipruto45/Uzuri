import axiosClient from "../../api/axiosClient";

export const fetchFees = async () => {
  const res = await axiosClient.get("fee-management/fees/");
  return res.data;
};

export const fetchStatements = async (studentId) => {
  const res = await axiosClient.get(
    `fee-management/statements/?student=${studentId}`,
  );
  return res.data;
};
