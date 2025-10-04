import axiosClient from "../../api/axiosClient";

// Endpoints mirror backend ai_support router (chatbot-conversations, study-recommendations, alerts)
export const listConversations = async () => {
  const res = await axiosClient.get("/ai-support/chatbot-conversations/");
  return res.data;
};

export const createConversation = async (payload) => {
  const res = await axiosClient.post(
    "/ai-support/chatbot-conversations/",
    payload,
  );
  return res.data;
};

export const listStudyRecommendations = async () => {
  const res = await axiosClient.get("/ai-support/study-recommendations/");
  return res.data;
};

export const createStudyRecommendation = async (payload) => {
  const res = await axiosClient.post(
    "/ai-support/study-recommendations/",
    payload,
  );
  return res.data;
};

export const listAlerts = async () => {
  const res = await axiosClient.get("/ai-support/alerts/");
  return res.data;
};

export const createAlert = async (payload) => {
  const res = await axiosClient.post("/ai-support/alerts/", payload);
  return res.data;
};

export const deleteAlert = async (id) => {
  const res = await axiosClient.delete(`/ai-support/alerts/${id}/`);
  return res.data;
};
