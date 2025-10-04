import React, { useEffect } from "react";
import { useDispatch } from "react-redux";
import DashboardLayout from "./layouts/DashboardLayout";
import AppRoutes from "./routes/AppRoutes";
import { fetchMe } from "./auth/authSlice";

export default function App() {
  const dispatch = useDispatch();

  useEffect(() => {
    // try to load current user if token exists
    const raw = localStorage.getItem("uzuri_auth");
    if (raw) {
      dispatch(fetchMe());
    }
  }, [dispatch]);

  return (
    <DashboardLayout>
      <AppRoutes />
    </DashboardLayout>
  );
}
