import React, { useEffect, useState } from "react";
import * as api from "./api";
import { useParams } from "react-router-dom";

const mapping = {
  users: api.listUsers,
  roles: api.listRoles,
  profiles: api.listProfiles,
  programs: api.listPrograms,
  courses: api.listCourses,
};

export default function ResourcePage() {
  const { resource } = useParams();
  const [items, setItems] = useState([]);
  useEffect(() => {
    let mounted = true;
    const fn = mapping[resource];
    if (!fn) {
      setItems([]);
      return;
    }
    fn().then((r) => {
      if (mounted) setItems(r || []);
    });
    return () => (mounted = false);
  }, [resource]);

  if (!mapping[resource]) {
    return (
      <div className="p-6">
        <h1 className="text-2xl font-semibold">Unknown resource</h1>
        <p className="text-sm text-gray-500 mt-2">
          The requested resource "{resource}" is not exposed by the frontend
          list view.
        </p>
      </div>
    );
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold mb-4">{resource}</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {items.map((it) => (
          <div key={it.id} className="p-3 bg-white rounded shadow">
            <pre className="text-xs whitespace-pre-wrap">
              {JSON.stringify(it, null, 2)}
            </pre>
          </div>
        ))}
      </div>
    </div>
  );
}
