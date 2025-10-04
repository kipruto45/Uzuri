import React, { useEffect, useState } from "react";
import PageShell from "../../components/ui/PageShell";
import { Card, CardContent } from "../../components/ui/Card";
import {
  listClearanceDocuments,
  uploadClearanceDocument,
  deleteClearanceDocument,
  downloadClearanceDocument,
  updateClearanceDocument,
  getClearanceDocument,
} from "./api";
import ClearanceList from "./components/ClearanceList";
import PreviewModal from "./components/PreviewModal";
import MetadataEditor from "./components/MetadataEditor";
import VersionsModal from "./components/VersionsModal";
import ClearanceUpload from "./components/ClearanceUpload";
import { DocumentIcon } from "./components/Icons";

export default function ClearancePage() {
  const [docs, setDocs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState("");

  useEffect(() => {
    let mounted = true;
    async function load() {
      setLoading(true);
      try {
        const data = await listClearanceDocuments();
        if (mounted) setDocs(data.results || data || []);
      } catch (e) {
        console.error("load failed", e);
      } finally {
        if (mounted) setLoading(false);
      }
    }
    load();
    return () => {
      mounted = false;
    };
  }, []);

  async function onUpload(fd) {
    try {
      const created = await uploadClearanceDocument(fd);
      setDocs((p) => [created, ...p]);
    } catch (e) {
      console.error("upload failed", e);
    }
  }

  async function onDelete(id) {
    try {
      await deleteClearanceDocument(id);
      setDocs((p) => p.filter((d) => d.id !== id));
    } catch (e) {
      console.error("delete failed", e);
    }
  }

  async function onDownload(id) {
    try {
      const blob = await downloadClearanceDocument(id);
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `document-${id}`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    } catch (e) {
      console.error("download failed", e);
    }
  }

  const [previewBlob, setPreviewBlob] = useState(null);
  const [previewName, setPreviewName] = useState("");
  const [previewOpen, setPreviewOpen] = useState(false);
  const [editorOpen, setEditorOpen] = useState(false);
  const [editingDoc, setEditingDoc] = useState(null);

  async function onPreview(id) {
    try {
      const blob = await downloadClearanceDocument(id);
      const doc = await getClearanceDocument(id);
      setPreviewBlob(blob);
      setPreviewName(doc.title || doc.file_name || `doc-${id}`);
      setPreviewOpen(true);
    } catch (e) {
      console.error("preview failed", e);
    }
  }

  function onEdit(doc) {
    setEditingDoc(doc);
    setEditorOpen(true);
  }

  async function onSaveMetadata(values) {
    if (!editingDoc) return;
    try {
      const updated = await updateClearanceDocument(editingDoc.id, values);
      setDocs((p) => p.map((d) => (d.id === updated.id ? updated : d)));
      setEditorOpen(false);
      setEditingDoc(null);
    } catch (e) {
      console.error("save metadata failed", e);
    }
  }

  function filtered() {
    const q = (query || "").trim().toLowerCase();
    if (!q) return docs;
    return docs.filter(
      (d) =>
        (d.title || "").toLowerCase().includes(q) ||
        (d.department || "").toLowerCase().includes(q),
    );
  }

  return (
    <PageShell
      title="Clearance Documents"
      subtitle="Upload and manage student clearance documents"
    >
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-blue-50 rounded">
            <DocumentIcon className="w-8 h-8 text-blue-600" />
          </div>
          <div>
            <p className="text-sm text-gray-600">
              Upload and manage student clearance documents
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search documents"
            className="border rounded px-3 py-2"
          />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <Card>
            <CardContent>
              {loading ? (
                <div>Loading…</div>
              ) : (
                <ClearanceList
                  docs={filtered()}
                  onDelete={onDelete}
                  onDownload={onDownload}
                  onEdit={onEdit}
                  onPreview={onPreview}
                />
              )}
            </CardContent>
          </Card>
        </div>

        <aside>
          <Card>
            <CardContent>
              <h2 className="text-sm font-medium mb-3">Upload Document</h2>
              <ClearanceUpload onUpload={onUpload} />
            </CardContent>
          </Card>
        </aside>
      </div>

      <PreviewModal
        open={previewOpen}
        fileBlob={previewBlob}
        fileName={previewName}
        onClose={() => setPreviewOpen(false)}
      />
      <MetadataEditor
        open={editorOpen}
        initial={editingDoc || {}}
        onClose={() => setEditorOpen(false)}
        onSave={onSaveMetadata}
      />
      <VersionsModal open={false} id={editingDoc?.id} onClose={() => {}} />
    </PageShell>
  );
}
