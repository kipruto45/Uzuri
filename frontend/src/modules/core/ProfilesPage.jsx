import React, { useEffect, useState } from "react";
import { listProfiles } from "./api";

export default function ProfilesPage() {
  const [profiles, setProfiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [q, setQ] = useState("");

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    listProfiles()
      .then((r) => {
        if (mounted) setProfiles(r || []);
      })
      .finally(() => {
        if (mounted) setLoading(false);
      });
    return () => (mounted = false);
  }, []);

  const filtered = profiles.filter((p) => {
    if (!q) return true;
    const s = (p.full_name || p.student_id || p.id || "")
      .toString()
      .toLowerCase();
    return s.includes(q.toLowerCase());
  });

  return (
    <div className="p-6">
      <header className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6">
        <div>
          <h1 className="text-2xl font-semibold">Student Profiles</h1>
          <p className="text-sm text-gray-500">
            Browse and manage student profiles
          </p>
        </div>
        <div className="flex items-center gap-2">
          <input
            placeholder="Search by name or student id"
            value={q}
            onChange={(e) => setQ(e.target.value)}
            className="border rounded px-3 py-2"
          />
        </div>
      </header>

      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {Array.from({ length: 6 }).map((_, i) => (
            <div
              key={i}
              className="p-4 bg-white rounded shadow animate-pulse"
            />
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map((p) => (
            <div key={p.id} className="p-4 bg-white rounded shadow">
              <div className="font-medium">
                {p.full_name || p.student_id || p.id}
              </div>
              <div className="text-xs text-gray-500 mt-1">
                Program: {p.program_name || "—"}
              </div>
              <div className="text-xs text-gray-500 mt-1">
                Status: {p.status || "—"}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
