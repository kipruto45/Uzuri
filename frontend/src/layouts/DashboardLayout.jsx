import React, { useEffect, useState } from "react";
import axiosClient from "../api/axiosClient";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

export default function DashboardLayout({ children }) {
  const [roles, setRoles] = useState([]);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    let mounted = true;
    (async () => {
      try {
        const res = await axiosClient.get("/core/roles/");
        if (mounted) setRoles(res.data || []);
      } catch (e) {
        // ignore
      }
    })();
    return () => (mounted = false);
  }, []);

  const isFinance = roles.includes("finance");
  const isStudent = roles.includes("student");

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar onToggle={() => setOpen(!open)} />
      <div className="flex">
        <Sidebar />
        <main className="flex-1 p-4">{children}</main>
      </div>
    </div>
  );
}
