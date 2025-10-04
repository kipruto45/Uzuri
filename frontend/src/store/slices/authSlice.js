import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  token:
    typeof window !== "undefined" ? localStorage.getItem("uzuri_token") : null,
  user: null,
};

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    setToken(state, action) {
      state.token = action.payload;
      if (typeof window !== "undefined")
        localStorage.setItem("uzuri_token", action.payload);
    },
    clearToken(state) {
      state.token = null;
      if (typeof window !== "undefined") localStorage.removeItem("uzuri_token");
    },
    setUser(state, action) {
      state.user = action.payload;
    },
  },
});

export const { setToken, clearToken, setUser } = authSlice.actions;
export default authSlice.reducer;
