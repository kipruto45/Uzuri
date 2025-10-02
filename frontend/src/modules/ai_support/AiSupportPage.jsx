import React, { useState } from 'react'
import { useConversations, useCreateConversation, useStudyRecommendations, useCreateRecommendation, useAlerts, useCreateAlert, useDeleteAlert } from '../../hooks/useAiSupport'

function Panel({ title, children }) {
  return (
    <div className="bg-white shadow-md rounded-lg p-4 flex-1">
      <h3 className="text-lg font-semibold mb-3">{title}</h3>
      {children}
    </div>
  )
}

export default function AiSupportPage() {
  // Poll conversations so UI picks up assistant responses when backend finishes processing
  const { data: convs = [], isLoading: convLoading } = useConversations({ refetchInterval: 3000 })
  const createConv = useCreateConversation()

  const { data: recs = [], isLoading: recLoading } = useStudyRecommendations()
  const createRec = useCreateRecommendation()

  const { data: alerts = [], isLoading: alertsLoading } = useAlerts()
  const createAL = useCreateAlert()
  const deleteAL = useDeleteAlert()

  const [message, setMessage] = useState('')
  const [recText, setRecText] = useState('')
  const [alertText, setAlertText] = useState('')

  return (
    <div className="container mx-auto p-4">
      <div className="mb-6">
        <h1 className="text-2xl font-bold">AI Support</h1>
        <p className="text-sm text-gray-600">Chat with the assistant, get study recommendations, and manage alerts.</p>
      </div>

      <div className="grid gap-4 grid-cols-1 lg:grid-cols-3">
        <Panel title="Chatbot">
          <div className="flex flex-col h-64">
            <div className="overflow-y-auto mb-3 flex-1 space-y-2">
              {convLoading ? (
                // Simple skeleton list
                <div className="space-y-2">
                  <div className="animate-pulse bg-gray-200 h-6 w-3/4 rounded" />
                  <div className="animate-pulse bg-gray-200 h-6 w-1/2 rounded" />
                </div>
              ) : convs.length === 0 ? (
                <div className="flex items-center gap-3 text-sm text-gray-500">
                  <svg className="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 10h.01M12 10h.01M16 10h.01M21 12c0 4.418-4.03 8-9 8-1.15 0-2.248-.163-3.25-.457L3 21l1.457-5.75C3.677 13.248 3 11.708 3 10a9 9 0 0118 0z"></path></svg>
                  No conversations yet. Try sending a question to the assistant.
                </div>
              ) : (
                convs.map((c) => (
                  <div key={c.id} className="bg-gray-50 p-2 rounded">
                    <div className="text-sm font-medium">You:</div>
                    <div className="text-sm mb-1">{c.message}</div>
                    <div className="text-sm font-medium">Assistant:</div>
                    <div className="text-sm text-gray-700">{c.response || '—'}</div>
                  </div>
                ))
              )}
            </div>

            <form
              onSubmit={(e) => {
                e.preventDefault()
                if (!message.trim()) return
                createConv.mutate({ message })
                setMessage('')
              }}
              className="flex gap-2 mt-2"
              aria-label="Chat with assistant"
            >
              <label htmlFor="ai-message" className="sr-only">Ask the assistant</label>
              <input id="ai-message" value={message} onChange={(e) => setMessage(e.target.value)} placeholder="Ask the assistant..." className="flex-1 border rounded p-2" aria-label="message input" />
              <button type="submit" className="bg-indigo-600 text-white px-4 py-2 rounded" aria-label="Send message">Send</button>
            </form>
          </div>
        </Panel>

        <Panel title="Study Recommendations">
          <div className="flex flex-col h-64">
            <div className="overflow-y-auto mb-3 flex-1 space-y-2">
              {recLoading ? (
                <div className="text-sm text-gray-500">Loading...</div>
              ) : recs.length === 0 ? (
                <div className="text-sm text-gray-500">No recommendations yet.</div>
              ) : (
                recs.map((r) => (
                  <div key={r.id} className="bg-gray-50 p-2 rounded">
                    <div className="text-sm text-gray-700">{r.recommendation}</div>
                    <div className="text-xs text-gray-400">{new Date(r.created_at).toLocaleString()}</div>
                  </div>
                ))
              )}
            </div>

            <form
              onSubmit={(e) => {
                e.preventDefault()
                if (!recText.trim()) return
                createRec.mutate({ recommendation: recText })
                setRecText('')
              }}
              className="flex gap-2 mt-2"
            >
              <input value={recText} onChange={(e) => setRecText(e.target.value)} placeholder="Add recommendation..." className="flex-1 border rounded p-2" />
              <button type="submit" className="bg-green-600 text-white px-4 py-2 rounded">Add</button>
            </form>
          </div>
        </Panel>

        <Panel title="Alerts">
          <div className="flex flex-col h-64">
            <div className="overflow-y-auto mb-3 flex-1 space-y-2">
              {alertsLoading ? (
                <div className="text-sm text-gray-500">Loading...</div>
              ) : alerts.length === 0 ? (
                <div className="text-sm text-gray-500">No alerts.</div>
              ) : (
                alerts.map((a) => (
                  <div key={a.id} className="bg-gray-50 p-2 rounded flex items-start justify-between">
                    <div>
                      <div className="text-sm text-gray-700">{a.message}</div>
                      <div className="text-xs text-gray-400">{new Date(a.created_at).toLocaleString()}</div>
                    </div>
                    <div className="ml-4 flex flex-col gap-2">
                      <button onClick={() => deleteAL.mutate(a.id)} className="text-sm text-red-600">Delete</button>
                    </div>
                  </div>
                ))
              )}
            </div>

            <form
              onSubmit={(e) => {
                e.preventDefault()
                if (!alertText.trim()) return
                createAL.mutate({ message: alertText })
                setAlertText('')
              }}
              className="flex gap-2 mt-2"
            >
              <input value={alertText} onChange={(e) => setAlertText(e.target.value)} placeholder="Create alert..." className="flex-1 border rounded p-2" />
              <button type="submit" className="bg-yellow-600 text-white px-4 py-2 rounded">Create</button>
            </form>
          </div>
        </Panel>
      </div>
    </div>
  )
}
