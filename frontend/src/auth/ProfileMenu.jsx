import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { logout } from './authSlice'

export default function ProfileMenu() {
  const dispatch = useDispatch()
  const user = useSelector((s) => s.auth.user)

  return (
    <div>
      {user ? (
        <div>
          <span>{user?.full_name || user?.email}</span>
          <button onClick={() => dispatch(logout())}>Logout</button>
        </div>
      ) : (
        <div>Not logged in</div>
      )}
    </div>
  )
}
