import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import * as api from './api'

export const loginUser = createAsyncThunk('auth/login', async (creds, thunkAPI) => {
  const data = await api.login(creds)
  return data
})

export const fetchMe = createAsyncThunk('auth/me', async () => {
  const data = await api.me()
  return data
})

const initialState = { user: null, access: null, refresh: null, status: 'idle' }

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    logout(state) {
      state.user = null
      state.access = null
      state.refresh = null
      localStorage.removeItem('uzuri_auth')
    },
    setTokens(state, action) {
      const { access, refresh } = action.payload
      state.access = access
      state.refresh = refresh
      localStorage.setItem('uzuri_auth', JSON.stringify({ access, refresh }))
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(loginUser.pending, (state) => {
        state.status = 'loading'
      })
      .addCase(loginUser.fulfilled, (state, action) => {
        state.status = 'succeeded'
        const access = action.payload?.access || action.payload?.token || null
        const refresh = action.payload?.refresh || null
        state.access = access
        state.refresh = refresh
        state.user = action.payload?.user || null
        localStorage.setItem('uzuri_auth', JSON.stringify({ access, refresh }))
      })
      .addCase(loginUser.rejected, (state) => {
        state.status = 'failed'
      })
      .addCase(fetchMe.fulfilled, (state, action) => {
        state.user = action.payload
      })
  },
})

export const { logout, setTokens } = authSlice.actions
export default authSlice.reducer
