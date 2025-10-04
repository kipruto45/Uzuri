import React, { useEffect, useState } from "react";
import api, { resolveApiUrl } from "../api/client";
import { useParams } from "react-router-dom";

export default function ResourceView() {
  const { name } = useParams();
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let mounted = true;
    async function load() {
      setLoading(true);
      try {
        // Fetch API root first to resolve the URL
        const root = await api.get("/api/");
        const url = root.data[name];
        if (!url) throw new Error("Resource not found in API root");
        const resolved = resolveApiUrl(url);
        const res = await api.get(resolved);
        if (mounted) setData(res.data);
      } catch (err) {
        setError(err.response ? err.response.data : err.message);
      } finally {
        setLoading(false);
      }
    }
    load();
    return () => {
      mounted = false;
    };
  }, [name]);

  if (loading) return <div>Loading…</div>;
  if (error)
    return (
      <pre style={{ color: "crimson" }}>{JSON.stringify(error, null, 2)}</pre>
    );
  if (!data) return <div>No data</div>;

  return (
    <div>
      <h2>Resource: {name}</h2>
      <pre style={{ whiteSpace: "pre-wrap" }}>
        {JSON.stringify(data, null, 2)}
      </pre>
    </div>
  );
}
