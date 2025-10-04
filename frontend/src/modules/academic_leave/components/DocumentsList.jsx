import React, { useState } from "react";
import { File, Image, FileText } from "lucide-react";
import PreviewModal from "./PreviewModal";

function IconForName(name) {
  const ext = name.split(".").pop()?.toLowerCase();
  if (["png", "jpg", "jpeg", "gif", "svg"].includes(ext))
    return <Image className="w-4 h-4 mr-2" />;
  if (["pdf", "doc", "docx", "txt"].includes(ext))
    return <FileText className="w-4 h-4 mr-2" />;
  return <File className="w-4 h-4 mr-2" />;
}

export default function DocumentsList({ docs = [] }) {
  const [open, setOpen] = useState(false);
  const [selected, setSelected] = useState(null);
  if (!docs.length)
    return <div className="text-sm text-gray-500">No documents</div>;

  return (
    <ul className="space-y-2">
      {docs.map((d) => (
        <li
          key={d.id}
          className="flex items-center justify-between p-2 border rounded-md bg-white dark:bg-gray-800"
        >
          <div className="flex items-center">
            {IconForName(d.name)}
            <div className="text-sm">
              <div className="font-medium">{d.name}</div>
              <div className="text-xs text-gray-500">
                Uploaded {new Date(d.uploaded_at).toLocaleString()}
              </div>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={() => {
                setSelected(d);
                setOpen(true);
              }}
              className="text-indigo-600 text-sm"
            >
              Preview
            </button>
            <a href={d.url} download className="text-gray-500 text-sm">
              Download
            </a>
          </div>
        </li>
      ))}

      <PreviewModal
        open={open}
        onClose={() => setOpen(false)}
        src={selected?.url}
        name={selected?.name}
      />
    </ul>
  );
}
