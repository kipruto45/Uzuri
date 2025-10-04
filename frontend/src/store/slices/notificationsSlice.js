import { createSlice } from "@reduxjs/toolkit";

const notificationsSlice = createSlice({
  name: "notifications",
  initialState: { items: [] },
  reducers: {
    pushNotification(state, action) {
      state.items.unshift(action.payload);
      if (state.items.length > 50) state.items.pop();
    },
    clearNotifications(state) {
      state.items = [];
    },
  },
});

export const { pushNotification, clearNotifications } =
  notificationsSlice.actions;
export default notificationsSlice.reducer;
