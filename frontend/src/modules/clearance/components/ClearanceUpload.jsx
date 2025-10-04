import React, { useRef, useState } from "react";

export default function ClearanceUpload({ onUpload }) {
  const ref = useRef(null);
  const [title, setTitle] = useState("");

  function onDrop(e) {
    e.preventDefault();
    const f = e.dataTransfer.files[0];
    if (f) handleFile(f);
  }

  function onFileChange(e) {
    const f = e.target.files[0];
    if (f) handleFile(f);
  }

  function handleFile(f) {
    // simple client-side validation
    const allowed = [
      "application/pdf",
      "image/png",
      "image/jpeg",
      "text/plain",
      "application/msword",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ];
    if (!allowed.includes(f.type)) {
      alert("Unsupported file type");
      return;
    }
    const fd = new FormData();
    fd.append("file", f);
    fd.append("title", title || f.name);
    onUpload(fd);
  }

  return (
    <div>
      <label className="block mb-2 text-sm">Title (optional)</label>
      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        className="w-full border rounded px-2 py-1 mb-3"
        placeholder="Document title"
      />
      <div
        onDragOver={(e) => e.preventDefault()}
        onDrop={onDrop}
        onClick={() => ref.current && ref.current.click()}
        role="button"
        tabIndex={0}
        onKeyDown={(e) =>
          e.key === "Enter" && ref.current && ref.current.click()
        }
        className="border-2 border-dashed rounded p-6 text-center bg-white"
      >
        <div className="text-sm text-gray-600">
          Drag & drop clearance documents here, or click to upload
        </div>
        <input
          ref={ref}
          type="file"
          className="hidden"
          onChange={onFileChange}
        />
      </div>
    </div>
  );
}
