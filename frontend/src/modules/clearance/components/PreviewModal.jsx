import React, { useEffect, useState, useRef } from "react";
import Lightbox from "../../../components/Lightbox";

export default function PreviewModal({ open, fileBlob, fileName, onClose }) {
  const [pdfUrl, setPdfUrl] = useState(null);
  const [imgUrl, setImgUrl] = useState(null);
  const [lightboxOpen, setLightboxOpen] = useState(false);
  const canvasRef = useRef(null);

  useEffect(() => {
    if (!fileBlob) return;
    const url = URL.createObjectURL(fileBlob);
    if (fileName && fileName.toLowerCase().endsWith(".pdf")) {
      setPdfUrl(url);
    } else {
      setImgUrl(url);
    }
    return () => {
      if (url) URL.revokeObjectURL(url);
      setPdfUrl(null);
      setImgUrl(null);
    };
  }, [fileBlob, fileName]);

  // Try to render first page using pdfjs for better cross-browser support
  useEffect(() => {
    let cancelled = false;
    async function renderPdf() {
      if (!pdfUrl || !canvasRef.current) return;
      try {
        // Use eval to avoid Vite attempting to pre-resolve the import during dev pre-bundling
        const pdfjsLib = await eval('import("pdfjs-dist/build/pdf")');
        // worker (guarded)
        try {
          const pdfjsWorker = await eval(
            'import("pdfjs-dist/build/pdf.worker.entry")',
          );
          // Some bundlers export a default path, handle both
          pdfjsLib.GlobalWorkerOptions.workerSrc =
            pdfjsWorker?.default || pdfjsWorker;
        } catch (e) {
          // ignore worker setup in environments where worker entry isn't resolvable
        }
        const loadingTask = pdfjsLib.getDocument(pdfUrl);
        const pdf = await loadingTask.promise;
        const page = await pdf.getPage(1);
        const viewport = page.getViewport({ scale: 1.0 });
        const canvas = canvasRef.current;
        const context = canvas.getContext("2d");
        canvas.height = viewport.height;
        canvas.width = viewport.width;
        const renderContext = { canvasContext: context, viewport };
        await page.render(renderContext).promise;
      } catch (e) {
        // Don't throw — failure to render PDF preview should not block the app or dev server
        console.debug("pdf rendering skipped or failed", e);
      }
    }
    if (pdfUrl) renderPdf();
    return () => {
      cancelled = true;
    };
  }, [pdfUrl]);

  if (!open) return null;
  return (
    <>
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
        <div className="bg-white rounded shadow-lg max-w-4xl w-full max-h-[90vh] overflow-auto p-4">
          <div className="flex justify-between items-center mb-2">
            <h3 className="font-medium">Preview — {fileName}</h3>
            <div className="flex items-center gap-2">
              {imgUrl && (
                <button
                  onClick={() => setLightboxOpen(true)}
                  className="px-2 py-1 border rounded"
                >
                  Open Lightbox
                </button>
              )}
              <button onClick={onClose} className="px-2 py-1 border rounded">
                Close
              </button>
            </div>
          </div>
          <div className="h-[70vh] flex items-center justify-center">
            {pdfUrl ? (
              <canvas ref={canvasRef} className="max-w-full max-h-full" />
            ) : imgUrl ? (
              <img src={imgUrl} alt={fileName} className="max-h-full mx-auto" />
            ) : (
              <div className="text-sm text-gray-500">No preview available</div>
            )}
          </div>
        </div>
      </div>
      <Lightbox
        open={lightboxOpen}
        src={imgUrl}
        alt={fileName}
        onClose={() => setLightboxOpen(false)}
      />
    </>
  );
}
