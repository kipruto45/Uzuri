import React, { useEffect, useState } from "react";
import { listRoles } from "./api";

export default function RolesPage() {
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [q, setQ] = useState("");

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    listRoles()
      .then((r) => {
        if (mounted) setRoles(r || []);
      })
      .finally(() => {
        if (mounted) setLoading(false);
      });
    return () => (mounted = false);
  }, []);

  const filtered = roles.filter(
    (r) => !q || (r.name || "").toLowerCase().includes(q.toLowerCase()),
  );

  return (
    <div className="p-6">
      <header className="flex items-center justify-between mb-4">
        <div>
          <h1 className="text-2xl font-semibold">Roles</h1>
          <p className="text-sm text-gray-500">
            Manage system roles and permissions
          </p>
        </div>
        <div className="flex items-center gap-2">
          <input
            placeholder="Filter roles"
            value={q}
            onChange={(e) => setQ(e.target.value)}
            className="border rounded px-3 py-2"
          />
          <button className="px-3 py-2 bg-indigo-600 text-white rounded">
            New Role
          </button>
        </div>
      </header>

      {loading ? (
        <div className="space-y-3">
          {Array.from({ length: 4 }).map((_, i) => (
            <div
              key={i}
              className="h-12 bg-white rounded shadow animate-pulse"
            />
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map((role) => (
            <div key={role.id} className="p-4 bg-white rounded shadow">
              <div className="font-medium">{role.name}</div>
              <div className="text-xs text-gray-500 mt-1">
                {role.description}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
