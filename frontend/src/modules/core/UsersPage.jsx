import React, { useEffect, useState } from "react";
import { listUsers } from "./api";

function Avatar({ name }) {
  const initials = (name || "")
    .split(" ")
    .map((s) => s[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();
  return (
    <div className="w-12 h-12 rounded-full bg-indigo-600 text-white flex items-center justify-center font-semibold">
      {initials || "U"}
    </div>
  );
}

export default function UsersPage() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState("");

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    listUsers()
      .then((r) => {
        if (mounted) setUsers(r || []);
      })
      .finally(() => {
        if (mounted) setLoading(false);
      });
    return () => {
      mounted = false;
    };
  }, []);

  const filtered = users.filter((u) => {
    const q = query.trim().toLowerCase();
    if (!q) return true;
    return (
      (u.username || u.email || "").toLowerCase().includes(q) ||
      (u.full_name || "").toLowerCase().includes(q)
    );
  });

  return (
    <div className="p-6">
      <header className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6">
        <div>
          <h1 className="text-2xl font-semibold">Users</h1>
          <p className="text-sm text-gray-500 mt-1">
            Manage platform users and their profiles
          </p>
        </div>
        <div className="flex items-center gap-2">
          <input
            aria-label="Search users"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search users or email"
            className="border rounded px-3 py-2 w-64"
          />
          <button className="px-3 py-2 bg-indigo-600 text-white rounded">
            New User
          </button>
        </div>
      </header>

      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="p-4 bg-white rounded shadow animate-pulse">
              <div className="h-3 bg-gray-200 rounded w-1/3 mb-3" />
              <div className="h-8 bg-gray-200 rounded w-full mb-2" />
              <div className="h-6 bg-gray-200 rounded w-2/3" />
            </div>
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map((user) => (
            <div
              key={user.id}
              className="p-4 bg-white rounded shadow flex items-center gap-4"
            >
              <Avatar name={user.full_name || user.username || user.email} />
              <div className="flex-1">
                <div className="font-medium">
                  {user.full_name || user.username || user.email}
                </div>
                <div className="text-sm text-gray-500">{user.email}</div>
                <div className="mt-2 text-xs text-gray-600">
                  Joined:{" "}
                  {user.date_joined
                    ? new Date(user.date_joined).toLocaleDateString()
                    : "—"}
                </div>
              </div>
              <div className="flex flex-col gap-2">
                <button className="px-3 py-1 border rounded text-sm">
                  View
                </button>
                <button className="px-3 py-1 bg-indigo-600 text-white rounded text-sm">
                  Message
                </button>
              </div>
            </div>
          ))}
          {filtered.length === 0 && (
            <div className="col-span-full text-center text-gray-500 py-8">
              No users match your search.
            </div>
          )}
        </div>
      )}
    </div>
  );
}
