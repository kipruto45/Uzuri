import React, { useEffect, useState } from "react";
import api from "../api/client";
import { Link } from "react-router-dom";

export default function Resources() {
  const [resources, setResources] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function load() {
      try {
        const res = await api.get("/api/");
        setResources(res.data);
      } catch (err) {
        setError(err.response ? err.response.data : err.message);
      }
    }
    load();
  }, []);

  if (error)
    return (
      <pre style={{ color: "crimson" }}>{JSON.stringify(error, null, 2)}</pre>
    );
  if (!resources) return <div>Loading resources…</div>;

  // resources is likely an object mapping names to urls
  return (
    <div>
      <h2>API Resources</h2>
      <ul>
        {Object.keys(resources).map((k) => (
          <li key={k}>
            <Link to={`/crud/${encodeURIComponent(k)}`}>{k}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
