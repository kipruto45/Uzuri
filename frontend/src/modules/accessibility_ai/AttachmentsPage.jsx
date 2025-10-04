import React, { useState, useEffect, useRef } from "react";
import { listAttachments, uploadAttachment } from "../attachments/api";
import axiosClient from "../../api/axiosClient";
import UploadArea from "./components/UploadArea";
import FileGrid from "./components/FileGrid";
import FileTable from "./components/FileTable";

export default function AttachmentsPage() {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [view, setView] = useState("grid"); // grid | table
  const [query, setQuery] = useState("");
  const [sortKey, setSortKey] = useState("date");
  const [sortDir, setSortDir] = useState("desc");

  useEffect(() => {
    let mounted = true;
    async function load() {
      setLoading(true);
      try {
        const data = await listAttachments();
        if (mounted) setFiles(data);
      } catch (e) {
        console.error("failed to load attachments", e);
      } finally {
        if (mounted) setLoading(false);
      }
    }
    load();
    return () => (mounted = false);
  }, []);

  async function onUpload(file, metadata = {}) {
    const fd = new FormData();
    fd.append("file", file);
    Object.keys(metadata).forEach((k) => fd.append(k, metadata[k]));
    const created = await uploadAttachment(fd);
    setFiles((prev) => [created, ...prev]);
  }

  async function onDelete(id) {
    try {
      await axiosClient.delete(`attachments/${id}/`);
      setFiles((prev) => prev.filter((f) => f.id !== id));
    } catch (e) {
      console.error("delete failed", e);
    }
  }

  async function onDownload(id) {
    try {
      // backend should return a download URL or stream; open in new tab
      const res = await axiosClient.get(`attachments/${id}/download/`);
      const url = res.data?.url || res.request?.responseURL;
      if (url) window.open(url, "_blank");
    } catch (e) {
      console.error("download failed", e);
    }
  }

  function filtered() {
    const q = query.trim().toLowerCase();
    let out = files.slice();
    if (q)
      out = out.filter(
        (f) =>
          (f.name || "").toLowerCase().includes(q) ||
          (f.type || "").toLowerCase().includes(q),
      );
    out.sort((a, b) => {
      const dir = sortDir === "asc" ? 1 : -1;
      if (sortKey === "name") return a.name.localeCompare(b.name) * dir;
      if (sortKey === "size") return (a.size - b.size) * dir;
      return (new Date(a.created_at) - new Date(b.created_at)) * dir;
    });
    return out;
  }

  return (
    <div className="p-6">
      <header className="mb-6 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold">
            Accessibility AI — Attachments
          </h1>
          <p className="text-sm text-gray-600">
            Upload and manage documents, images, and other files. OCR and
            alt-text support available.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <input
            aria-label="Search files"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search files"
            className="border rounded px-3 py-2"
          />
          <select
            aria-label="View mode"
            value={view}
            onChange={(e) => setView(e.target.value)}
            className="border rounded px-2 py-2"
          >
            <option value="grid">Grid</option>
            <option value="table">Table</option>
          </select>
          <select
            aria-label="Sort by"
            value={sortKey}
            onChange={(e) => setSortKey(e.target.value)}
            className="border rounded px-2 py-2"
          >
            <option value="date">Date</option>
            <option value="name">Name</option>
            <option value="size">Size</option>
          </select>
          <button
            aria-pressed={sortDir === "asc"}
            onClick={() => setSortDir((s) => (s === "asc" ? "desc" : "asc"))}
            className="border rounded px-3 py-2"
          >
            {sortDir === "asc" ? "Asc" : "Desc"}
          </button>
        </div>
      </header>

      <UploadArea onUpload={onUpload} />

      <main className="mt-6">
        {loading ? (
          <div className="text-gray-500">Loading attachments…</div>
        ) : view === "grid" ? (
          <FileGrid
            files={filtered()}
            onDelete={onDelete}
            onDownload={onDownload}
          />
        ) : (
          <FileTable
            files={filtered()}
            onDelete={onDelete}
            onDownload={onDownload}
          />
        )}
      </main>
    </div>
  );
}
