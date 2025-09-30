import React, { useState, useRef } from 'react'
import Dialog from '../../../components/ui/Dialog'
import { motion } from 'framer-motion'
import { createLeaveRequest, uploadLeaveDocument } from '../api'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { Paperclip } from 'lucide-react'
import toast from 'react-hot-toast'

function FileDrop({ onChange, maxSizeMB = 10, allowedTypes = null }) {
  const fileRef = useRef()
  const [files, setFiles] = useState([]) // { file, error }

  const validate = (file) => {
    const errors = []
    const maxBytes = maxSizeMB * 1024 * 1024
    if (file.size > maxBytes) errors.push(`File too large (max ${maxSizeMB}MB)`)
    if (allowedTypes && allowedTypes.length) {
      const ok = allowedTypes.some((t) => file.type === t || file.name.toLowerCase().endsWith(t.replace('application/', '.')))
      if (!ok) errors.push('File type not allowed')
    }
    return errors.length ? errors.join('; ') : null
  }

  const handleFiles = (f) => {
    const list = Array.from(f).map((file) => ({ file, error: validate(file) }))
    setFiles(list)
    onChange && onChange(list)
  }

  const removeAt = (i) => {
    const next = files.slice(0)
    next.splice(i, 1)
    setFiles(next)
    onChange && onChange(next)
  }

  return (
    <div className="mt-2">
      <div className="border-2 border-dashed border-gray-200 dark:border-gray-700 rounded-md p-4 text-center">
        <div className="flex items-center justify-center text-gray-500 dark:text-gray-400">
          <Paperclip className="w-6 h-6 mr-2" />
          <div>
            <div className="font-medium">Drag & drop files here</div>
            <div className="text-xs">or <button type="button" className="text-indigo-600" onClick={() => fileRef.current.click()}>browse</button></div>
          </div>
        </div>
        <input ref={fileRef} type="file" className="hidden" onChange={(e) => handleFiles(e.target.files)} multiple />
      </div>

      {files.length > 0 && (
        <ul className="mt-2 text-sm space-y-2">
          {files.map(({ file, error }, i) => (
            <li key={i} className="flex items-center justify-between p-2 border rounded bg-white dark:bg-gray-800">
              <div>
                <div className="font-medium">{file.name}</div>
                <div className="text-xs text-gray-500">{Math.round(file.size / 1024)} KB {error ? <span className="text-red-600">• {error}</span> : null}</div>
              </div>
              <div className="flex items-center space-x-2">
                <button type="button" onClick={() => removeAt(i)} className="text-xs text-red-600">Remove</button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

export default function NewRequestModal({ isOpen, onClose }) {
  const [step, setStep] = useState(0)
  const selectRef = useRef(null)
  const [form, setForm] = useState({ leave_type: '', start_date: '', end_date: '', reason: '' })
  const [files, setFiles] = useState([])
  const [previewOpen, setPreviewOpen] = useState(false)
  const [previewFile, setPreviewFile] = useState(null)
  const qc = useQueryClient()

  // allowed file types: pdf, images, docx
  const allowedTypes = ['application/pdf', 'image/png', 'image/jpeg', 'image/webp', '.docx', '.doc']

  const mutation = useMutation(createLeaveRequest, {
    onSuccess: async (data) => {
      // upload files if present (files is array of {file, error})
      if (files.length) {
        // persist request id for potential retry actions
        setCurrentRequestId(data.id)
        setUploading(true)
        // Compute combined progress by aggregating per-file loaded/total
        const totalBytes = files.reduce((s, e) => s + (e.file?.size || 0), 0)
        const perFileLoaded = {}

        for (let i = 0; i < files.length; i++) {
          const entry = files[i]
          if (entry.error) continue
          const f = entry.file
          const fd = new FormData()
          fd.append('file', f)
          try {
            await uploadLeaveDocument(data.id, fd, (ev) => {
              // update per-file loaded
              perFileLoaded[i] = ev.loaded
              const loadedSum = Object.values(perFileLoaded).reduce((a, b) => a + b, 0)
              const pct = totalBytes ? Math.round((loadedSum / totalBytes) * 100) : 0
              setCombinedProgress(pct)
              const filePct = ev.total ? Math.round((ev.loaded / ev.total) * 100) : 0
              setUploadProgress((prev) => ({ ...prev, [i]: filePct }))
            })
          } catch (err) {
            console.error('upload error', err)
            setFileErrors((prev) => ({ ...prev, [i]: 'Upload failed' }))
          }
        }
        setCombinedProgress(100)
        setUploading(false)
      }
      qc.invalidateQueries(['leaveRequests'])
      toast.success('Request submitted')
      onClose()
    },
    onError: () => toast.error('Failed to submit')
  })

  const [errors, setErrors] = useState({})
  const [fileErrors, setFileErrors] = useState({})
  const [uploadProgress, setUploadProgress] = useState({})
  const [combinedProgress, setCombinedProgress] = useState(0)
  const [uploading, setUploading] = useState(false)
  const [currentRequestId, setCurrentRequestId] = useState(null)

  const validateStep = (s) => {
    const err = {}
    if (s === 0) {
      if (!form.leave_type) err.leave_type = 'Select a leave type'
      if (!form.start_date) err.start_date = 'Start date required'
      if (!form.end_date) err.end_date = 'End date required'
      if (form.start_date && form.end_date && new Date(form.end_date) < new Date(form.start_date)) err.end_date = 'End date must be after start date'
      if (!form.reason || form.reason.length < 10) err.reason = 'Reason must be at least 10 characters'
    }
    setErrors(err)
    return Object.keys(err).length === 0
  }

  const submit = async (e) => {
    e && e.preventDefault()
    if (step === 0) {
      if (!validateStep(0)) return
      setStep(1)
      return
    }
    if (step === 1) {
      // proceed to review (validate files)
      const ferr = {}
      const anyGood = files && files.some((f) => !f.error)
      if (!anyGood) {
        ferr.files = 'Please attach at least one supporting document or proceed without files.'
      }
      setFileErrors(ferr)
      if (Object.keys(ferr).length) return
      setStep(2)
      return
    }
    // step === 2 -> final submit
    mutation.mutate(form)
  }

  // helper to retry upload for a single file index (used by UI retry)
  const retryUpload = async (requestId, index) => {
    const entry = files[index]
    if (!entry || entry.error) return
    const f = entry.file
    const fd = new FormData()
    fd.append('file', f)
    // clear previous error for this index
    setFileErrors((prev) => {
      const copy = { ...prev }
      delete copy[index]
      return copy
    })
    try {
      const rid = requestId || currentRequestId
      if (!rid) {
        toast('Please submit the request first to upload attachments')
        return
      }
      await uploadLeaveDocument(rid, fd, (ev) => {
        const pct = ev.total ? Math.round((ev.loaded / ev.total) * 100) : 0
        setUploadProgress((prev) => ({ ...prev, [index]: pct }))
      })
    } catch (err) {
      setFileErrors((prev) => ({ ...prev, [index]: 'Upload failed' }))
    }
  }

  return (
    <Dialog open={isOpen} onClose={onClose} className="" initialFocus={selectRef}>
      <div className="min-h-screen px-4 text-center">
        <Dialog.Overlay className="fixed inset-0 bg-black opacity-30" />

        <span className="inline-block h-screen align-middle" aria-hidden="true">&#8203;</span>
        <motion.div initial={{ scale: 0.98, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} className="inline-block w-full max-w-xl p-6 my-8 overflow-hidden align-middle transition-all transform bg-white dark:bg-gray-900 shadow-xl rounded-2xl">
          <Dialog.Title className="text-lg font-medium">New Leave Request</Dialog.Title>

          <div className="mt-3 mb-4">
            <div className="flex items-center space-x-3">
              <div className={`text-xs ${step===0? 'font-semibold':''}`}>1. Details</div>
              <div className={`text-xs ${step===1? 'font-semibold':''}`}>2. Documents</div>
              <div className={`text-xs ${step===2? 'font-semibold':''}`}>3. Review</div>
            </div>
            <div className="h-1 bg-gray-100 rounded mt-2 overflow-hidden">
              <div className={`h-1 bg-indigo-600`} style={{ width: step===0? '30%': step===1? '66%': '100%' }} />
            </div>
          </div>

          <form onSubmit={submit} className="mt-4">
            {step === 0 && (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium">Leave type</label>
                  <select ref={selectRef} required value={form.leave_type} onChange={(e) => setForm({ ...form, leave_type: e.target.value })} className="mt-1 block w-full rounded-md border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
                    <option value="">Select type</option>
                    <option value="medical">Medical</option>
                    <option value="personal">Personal</option>
                    <option value="academic">Academic</option>
                  </select>
                  {errors.leave_type && <div className="text-xs text-red-600 mt-1">{errors.leave_type}</div>}
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-sm">Start date</label>
                    <input required type="date" value={form.start_date} onChange={(e) => setForm({ ...form, start_date: e.target.value })} className="mt-1 block w-full rounded-md border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800" />
                    {errors.start_date && <div className="text-xs text-red-600 mt-1">{errors.start_date}</div>}
                  </div>
                  <div>
                    <label className="block text-sm">End date</label>
                    <input required type="date" value={form.end_date} onChange={(e) => setForm({ ...form, end_date: e.target.value })} className="mt-1 block w-full rounded-md border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800" />
                    {errors.end_date && <div className="text-xs text-red-600 mt-1">{errors.end_date}</div>}
                  </div>
                </div>

                <div>
                  <label className="block text-sm">Reason</label>
                  <textarea required rows={4} value={form.reason} onChange={(e) => setForm({ ...form, reason: e.target.value })} className="mt-1 block w-full rounded-md border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800" />
                  <div className="text-xs text-gray-400 mt-1">{form.reason.length} characters</div>
                  {errors.reason && <div className="text-xs text-red-600 mt-1">{errors.reason}</div>}
                </div>
              </div>
            )}

            {step === 1 && (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm">Supporting documents</label>
                  <FileDrop onChange={setFiles} allowedTypes={allowedTypes} />
                  {fileErrors.files && <div className="text-xs text-red-600 mt-1">{fileErrors.files}</div>}
                </div>

                <div className="text-sm text-gray-500">You can add multiple documents. After submission, files will be attached to your request.</div>

                {files.length > 0 && (
                  <div className="space-y-2">
                    {files.map((fobj, idx) => (
                      <div key={idx} className="flex items-center justify-between p-2 border rounded bg-white dark:bg-gray-800">
                        <div>
                          <div className="font-medium">{fobj.file.name}</div>
                          <div className="text-xs text-gray-500">{Math.round(fobj.file.size / 1024)} KB {fobj.error ? <span className="text-red-600">• {fobj.error}</span> : null}</div>
                        </div>
                        <div className="w-48 text-right">
                          {uploadProgress[idx] ? (
                            <div className="text-xs">Uploading: {uploadProgress[idx]}%</div>
                          ) : fileErrors[idx] ? (
                            <div className="text-xs text-red-600">{fileErrors[idx]} <button type="button" onClick={() => retryUpload(null, idx)} className="ml-2 text-indigo-600 text-xs">Retry</button></div>
                          ) : (
                            <div className="text-xs text-gray-500">Ready</div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {step === 2 && (
              <div className="space-y-4">
                <h3 className="text-sm font-medium">Review your request</h3>
                <div className="p-3 border rounded">
                  <div><strong>Type:</strong> {form.leave_type}</div>
                  <div><strong>Dates:</strong> {form.start_date} → {form.end_date}</div>
                  <div className="mt-2"><strong>Reason:</strong><div className="text-sm mt-1">{form.reason}</div></div>
                  <div className="mt-2"><strong>Files:</strong> {files.length} file(s)</div>
                </div>
                <div className="text-sm text-gray-500">When you submit, your request and its documents will be uploaded.</div>

                  {files.length > 0 && (
                    <div className="mt-2 space-y-2">
                      {files.map((fobj, idx) => (
                        <div key={idx} className="p-2 border rounded bg-white dark:bg-gray-800">
                          <div className="flex items-center justify-between">
                            <div className="text-sm font-medium">{fobj.file.name}</div>
                            <div className="text-xs text-gray-500">{Math.round(fobj.file.size / 1024)} KB</div>
                          </div>
                          <div className="mt-2">
                            <div className="w-full h-2 bg-gray-100 rounded overflow-hidden">
                              <div className="h-2 bg-indigo-600" style={{ width: `${uploadProgress[idx] || 0}%` }} />
                            </div>
                            <div className="flex items-center justify-between mt-1">
                              <div className="text-xs text-gray-500">{uploadProgress[idx] ? `${uploadProgress[idx]}%` : fileErrors[idx] ? <span className="text-red-600">{fileErrors[idx]}</span> : 'Pending'}</div>
                              <div>
                                {fileErrors[idx] ? (
                                  <>
                                    <button type="button" onClick={() => retryUpload(/*requestId set after submit*/ null, idx)} className="text-xs text-indigo-600 mr-2">Retry</button>
                                  </>
                                ) : null}
                              </div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}

                {/* Combined progress bar while uploading */}
                {mutation.isLoading && (
                  <div className="mt-3">
                    <div className="text-xs text-gray-500 mb-1">Uploading documents: {combinedProgress}%</div>
                    <div className="w-full h-2 bg-gray-100 rounded overflow-hidden">
                      <div className="h-2 bg-indigo-600" style={{ width: `${combinedProgress}%` }} />
                    </div>
                  </div>
                )}
              </div>
            )}

            <div className="flex justify-between mt-6">
              <div>
                {step === 1 && <button type="button" onClick={() => setStep(0)} className="px-3 py-2 rounded-md border">Back</button>}
              </div>
              <div className="flex items-center space-x-2">
                <button type="button" onClick={onClose} className="px-4 py-2 rounded-md border">Cancel</button>
                <button type="submit" disabled={mutation.isLoading} className="px-4 py-2 rounded-md bg-gradient-to-r from-indigo-600 to-indigo-400 text-white flex items-center space-x-2">
                  {mutation.isLoading ? <svg className="animate-spin h-4 w-4 mr-2" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path></svg> : null}
                  <span>{step === 0 ? 'Next' : 'Submit'}</span>
                </button>
              </div>
            </div>
          </form>
        </motion.div>
      </div>
    </Dialog>
  )
}
