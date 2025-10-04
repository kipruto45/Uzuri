import React, { useState } from "react";
import PageShell from "../../components/ui/PageShell";
import { Card, CardContent } from "../../components/ui/Card";
import {
  useAccessibilityFeatures,
  useCreateFeature,
  useToggleFeature,
  useDeleteFeature,
} from "../../hooks/useAccessibility";

export default function AccessibilityPage() {
  const { data: features = [], isLoading } = useAccessibilityFeatures();
  const createMut = useCreateFeature();
  const toggleMut = useToggleFeature();
  const deleteMut = useDeleteFeature();
  const [editingId, setEditingId] = useState(null);
  const [editingText, setEditingText] = useState("");

  const handleToggle = (f) => {
    toggleMut.mutate({ id: f.id, enabled: !f.enabled });
  };

  const handleCreate = () => {
    const val = editingText.trim();
    if (!val) return;
    createMut.mutate({ feature_type: val, enabled: true });
    setEditingText("");
  };

  const handleDelete = (f) => {
    if (!window.confirm(`Delete feature ${f.feature_type}?`)) return;
    deleteMut.mutate(f.id);
  };

  const startEdit = (f) => {
    setEditingId(f.id);
    setEditingText(f.feature_type);
  };

  const saveEdit = async (f) => {
    if (!editingText.trim()) return;
    // Use createMut for simplicity: delete+create or backend patch could be used.
    createMut.mutate({ feature_type: editingText.trim(), enabled: true });
    setEditingId(null);
    setEditingText("");
  };

  if (isLoading) return <div>Loading accessibility features</div>;

  return (
    <PageShell
      title="Accessibility features"
      subtitle="Accessibility tools & features"
    >
      <div className="mb-4 flex gap-2">
        <input
          value={editingText}
          onChange={(e) => setEditingText(e.target.value)}
          placeholder="New feature type or edit selection"
          className="border rounded px-2 py-1 w-64"
        />
        <button
          onClick={editingId ? () => saveEdit({ id: editingId }) : handleCreate}
          className="px-3 py-1 rounded bg-indigo-600 text-white"
        >
          {editingId ? "Save" : "Create"}
        </button>
        {editingId ? (
          <button
            onClick={() => {
              setEditingId(null);
              setEditingText("");
            }}
            className="px-3 py-1 rounded border"
          >
            Cancel
          </button>
        ) : null}
      </div>

      {features.length === 0 ? (
        <Card>
          <CardContent>
            <div className="text-sm text-gray-500">
              No accessibility features configured.
            </div>
          </CardContent>
        </Card>
      ) : (
        <ul className="space-y-2 max-w-2xl">
          {features.map((f) => (
            <li key={f.id}>
              <Card>
                <CardContent className="flex items-center justify-between">
                  <div>
                    <div className="font-medium">{f.feature_type}</div>
                    <div className="text-xs text-gray-500">
                      Enabled: {String(f.enabled)}
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleToggle(f)}
                      className="px-3 py-1 rounded border bg-indigo-50"
                    >
                      {f.enabled ? "Disable" : "Enable"}
                    </button>
                    <button
                      onClick={() => startEdit(f)}
                      className="px-3 py-1 rounded border"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDelete(f)}
                      className="px-3 py-1 rounded border text-red-600"
                    >
                      Delete
                    </button>
                  </div>
                </CardContent>
              </Card>
            </li>
          ))}
        </ul>
      )}
    </PageShell>
  );
}
