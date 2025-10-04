import React, { useEffect, useState, useCallback } from "react";
import api from "../api/client";
import AttachmentUpload from "../components/AttachmentUpload";

export default function Attachments() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.get("/api/attachments/");
      setItems(res.data);
    } catch (err) {
      setError(err.response ? err.response.data : err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    let mounted = true;
    if (mounted) load();
    return () => {
      mounted = false;
    };
  }, [load]);

  return (
    <div>
      <h2>Attachments</h2>
      <AttachmentUpload onUploaded={load} />

      {loading && <div>Loading…</div>}
      {error && (
        <pre style={{ color: "crimson" }}>{JSON.stringify(error, null, 2)}</pre>
      )}
      {!loading && !error && (
        <ul>
          {Array.isArray(items) ? (
            items.map((it) => (
              <li key={it.id} style={{ marginBottom: 8 }}>
                <strong>{it.title || it.file || `#${it.id}`}</strong>
                {it.file && (
                  <span>
                    {" "}
                    —{" "}
                    <a href={it.file} target="_blank" rel="noreferrer">
                      Download
                    </a>
                  </span>
                )}
                <div style={{ fontSize: 12, color: "#666" }}>
                  {it.description || ""}
                </div>
              </li>
            ))
          ) : (
            <pre>{JSON.stringify(items, null, 2)}</pre>
          )}
        </ul>
      )}
    </div>
  );
}
