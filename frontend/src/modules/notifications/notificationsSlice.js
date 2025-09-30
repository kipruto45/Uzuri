import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import * as api from './api'

export const loadNotifications = createAsyncThunk('notifications/load', async () => {
  return await api.fetchNotifications()
})

const slice = createSlice({
  name: 'notifications',
  initialState: { items: [], status: 'idle' },
  reducers: {},
  extraReducers: (b) => {
    b.addCase(loadNotifications.fulfilled, (s, a) => {
      s.items = a.payload || []
      s.status = 'succeeded'
    })
  }
})

export default slice.reducer
