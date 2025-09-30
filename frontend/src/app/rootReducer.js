import { combineReducers } from 'redux'
import authReducer from '../auth/authSlice'
import notificationsReducer from '../modules/notifications/notificationsSlice'

const rootReducer = combineReducers({
  auth: authReducer,
  notifications: notificationsReducer,
})

export default rootReducer
