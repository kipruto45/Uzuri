import React, { useRef } from "react";

export default function UploadArea({ onUpload }) {
  const fileRef = useRef(null);

  function onDrop(e) {
    e.preventDefault();
    const f = e.dataTransfer.files[0];
    if (f) onUpload(f);
  }

  function onFileChange(e) {
    const f = e.target.files[0];
    if (f) onUpload(f);
  }

  return (
    <div>
      <div
        onDragOver={(e) => e.preventDefault()}
        onDrop={onDrop}
        role="button"
        tabIndex={0}
        className="border-2 border-dashed rounded p-6 text-center text-gray-600 bg-white"
        onClick={() => fileRef.current && fileRef.current.click()}
        onKeyDown={(e) =>
          e.key === "Enter" && fileRef.current && fileRef.current.click()
        }
        aria-label="Upload files"
      >
        <div className="text-lg font-medium">Drag & drop files here</div>
        <div className="text-sm">
          or click to select files (PDF, DOCX, TXT, CSV, images)
        </div>
        <input
          ref={fileRef}
          type="file"
          className="hidden"
          onChange={onFileChange}
        />
      </div>
    </div>
  );
}
