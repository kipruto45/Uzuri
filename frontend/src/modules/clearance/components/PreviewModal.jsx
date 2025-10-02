import React, { useEffect, useState, useRef } from 'react'
import Lightbox from '../../../components/Lightbox'

export default function PreviewModal({ open, fileBlob, fileName, onClose }) {
  const [pdfUrl, setPdfUrl] = useState(null)
  const [imgUrl, setImgUrl] = useState(null)
  const [lightboxOpen, setLightboxOpen] = useState(false)
  const canvasRef = useRef(null)

  useEffect(() => {
    if (!fileBlob) return
    const url = URL.createObjectURL(fileBlob)
    if (fileName && fileName.toLowerCase().endsWith('.pdf')) {
      setPdfUrl(url)
    } else {
      setImgUrl(url)
    }
    return () => {
      if (url) URL.revokeObjectURL(url)
      setPdfUrl(null)
      setImgUrl(null)
    }
  }, [fileBlob, fileName])

  // Try to render first page using pdfjs for better cross-browser support
  useEffect(() => {
    let cancelled = false
    async function renderPdf() {
      if (!pdfUrl || !canvasRef.current) return
      try {
        const pdfjsLib = await import('pdfjs-dist/build/pdf')
        // worker
        try {
          const pdfjsWorker = await import('pdfjs-dist/build/pdf.worker.entry')
          pdfjsLib.GlobalWorkerOptions.workerSrc = pdfjsWorker
        } catch (e) {
          // ignore worker setup on test env
        }
        const loadingTask = pdfjsLib.getDocument(pdfUrl)
        const pdf = await loadingTask.promise
        const page = await pdf.getPage(1)
        const viewport = page.getViewport({ scale: 1.0 })
        const canvas = canvasRef.current
        const context = canvas.getContext('2d')
        canvas.height = viewport.height
        canvas.width = viewport.width
        const renderContext = { canvasContext: context, viewport }
        await page.render(renderContext).promise
      } catch (e) {
        console.error('pdf rendering failed', e)
      }
    }
    if (pdfUrl) renderPdf()
    return () => { cancelled = true }
  }, [pdfUrl])

  if (!open) return null
  return (
    <>
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
        <div className="bg-white rounded shadow-lg max-w-4xl w-full max-h-[90vh] overflow-auto p-4">
          <div className="flex justify-between items-center mb-2">
            <h3 className="font-medium">Preview — {fileName}</h3>
            <div className="flex items-center gap-2">
              {imgUrl && (
                <button onClick={() => setLightboxOpen(true)} className="px-2 py-1 border rounded">Open Lightbox</button>
              )}
              <button onClick={onClose} className="px-2 py-1 border rounded">Close</button>
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
      <Lightbox open={lightboxOpen} src={imgUrl} alt={fileName} onClose={() => setLightboxOpen(false)} />
    </>
  )
}
