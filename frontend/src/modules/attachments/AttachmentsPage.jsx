import React, { useEffect, useState } from "react";
import PageShell from "../../components/ui/PageShell";
import { Card, CardContent } from "../../components/ui/Card";
import { listAttachments, uploadAttachment } from "./api";

export default function AttachmentsPage() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    (async () => {
      const data = await listAttachments();
      setItems(data || []);
    })();
  }, []);

  const onUpload = async (e) => {
    const file = e.target.files[0];
    const fd = new FormData();
    fd.append("file", file);
    await uploadAttachment(fd);
    const data = await listAttachments();
    setItems(data || []);
  };

  return (
    <PageShell title="Attachments" subtitle="Upload and manage your files">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <Card>
            <CardContent>
              <div className="mb-4">
                <label className="block text-sm font-medium mb-2">
                  Upload file
                </label>
                <input
                  type="file"
                  onChange={onUpload}
                  className="border rounded p-2"
                />
              </div>

              {items.length === 0 ? (
                <div className="text-sm text-gray-500">No attachments yet.</div>
              ) : (
                <ul className="space-y-2">
                  {items.map((a) => (
                    <li key={a.id} className="p-3 border rounded bg-white">
                      <div className="font-medium">{a.title || a.file}</div>
                      <div className="text-xs text-gray-500">
                        {a.created_at
                          ? new Date(a.created_at).toLocaleString()
                          : ""}
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </CardContent>
          </Card>
        </div>
        <aside>
          <Card>
            <CardContent>
              <div className="text-sm text-gray-600">Quick actions</div>
              <div className="mt-3 space-y-2">
                <button className="w-full px-3 py-2 rounded border">
                  Download all
                </button>
                <button className="w-full px-3 py-2 rounded border">
                  Clear temp uploads
                </button>
              </div>
            </CardContent>
          </Card>
        </aside>
      </div>
    </PageShell>
  );
}
