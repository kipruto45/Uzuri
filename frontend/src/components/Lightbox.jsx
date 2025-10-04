import React, { useEffect } from "react";

export default function Lightbox({ open, src, alt, onClose, children }) {
  useEffect(() => {
    function onKey(e) {
      if (e.key === "Escape") onClose();
    }
    if (open) {
      document.addEventListener("keydown", onKey);
      document.body.style.overflow = "hidden";
    }
    return () => {
      document.removeEventListener("keydown", onKey);
      document.body.style.overflow = "";
    };
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div className="fixed inset-0 bg-black/60 z-60 flex items-center justify-center p-4">
      <div className="relative bg-transparent max-w-[95vw] max-h-[95vh]">
        <button
          aria-label="Close"
          onClick={onClose}
          className="absolute right-2 top-2 z-10 text-white bg-black/30 px-2 py-1 rounded"
        >
          ✕
        </button>
        <div className="flex items-center justify-center max-w-full max-h-full">
          {src ? (
            <img
              src={src}
              alt={alt}
              className="max-w-full max-h-[90vh] object-contain"
            />
          ) : (
            children || <div className="text-white">No preview</div>
          )}
        </div>
      </div>
    </div>
  );
}
