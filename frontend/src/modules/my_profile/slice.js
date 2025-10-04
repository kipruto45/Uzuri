import { createSlice } from "@reduxjs/toolkit";

const slice = createSlice({
  name: "profile",
  initialState: { profile: null },
  reducers: {
    setProfile(state, action) {
      state.profile = action.payload;
    },
  },
});

export const { setProfile } = slice.actions;
export default slice.reducer;
