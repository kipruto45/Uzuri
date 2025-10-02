import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useEffect } from 'react'
import {
  listConversations,
  createConversation,
  listStudyRecommendations,
  createStudyRecommendation,
  listAlerts,
  createAlert,
  deleteAlert,
} from '../modules/ai_support/api'

export function useConversations(queryOptions = {}) {
  const q = useQuery(['ai-support', 'conversations'], listConversations, { staleTime: 1000 * 20, ...queryOptions })

  // Optional WebSocket live updates: if queryOptions.websocket is true and
  // there is a configured WS base, open a ws that triggers refetch on updates.
  useEffect(() => {
    const { websocket } = queryOptions || {}
    if (!websocket) return undefined
    const WS_BASE = process.env.VITE_WS_BASE || process.env.REACT_APP_WS_BASE || ''
    if (!WS_BASE) return undefined
    let ws
    try {
      ws = new WebSocket(WS_BASE.replace(/^http/, 'ws') + '/ai-support/updates/')
      ws.onopen = () => {
        // subscribe or log
      }
      ws.onmessage = (ev) => {
        try {
          const data = JSON.parse(ev.data)
          // Expect messages with type: 'conversations.updated' or similar
          if (data?.type && data.type.includes('conversation')) {
            q.refetch()
          }
        } catch (e) {
          // ignore parsing errors
        }
      }
      ws.onerror = () => {
        // no-op: allow polling fallback
      }
    } catch (e) {
      // ignore websocket errors; polling will handle updates
    }

    return () => {
      try {
        if (ws && ws.readyState === WebSocket.OPEN) ws.close()
      } catch (e) {}
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [queryOptions.websocket])

  return q

}

export function useCreateConversation() {
  const qc = useQueryClient()
  return useMutation((payload) => createConversation(payload), {
    onMutate: async (newConv) => {
      await qc.cancelQueries(['ai-support', 'conversations'])
      const previous = qc.getQueryData(['ai-support', 'conversations'])
      qc.setQueryData(['ai-support', 'conversations'], (old = []) => [
        ...(old || []),
        { id: Math.random() * -1, ...newConv, response: 'Thinking...' },
      ])
      return { previous }
    },
    onError: (err, newConv, context) => qc.setQueryData(['ai-support', 'conversations'], context.previous),
    onSettled: () => qc.invalidateQueries(['ai-support', 'conversations']),
  })
}

export function useStudyRecommendations() {
  return useQuery(['ai-support', 'recommendations'], listStudyRecommendations, { staleTime: 1000 * 60 })
}

export function useCreateRecommendation() {
  const qc = useQueryClient()
  return useMutation((payload) => createStudyRecommendation(payload), {
    onSuccess: () => qc.invalidateQueries(['ai-support', 'recommendations']),
  })
}

export function useAlerts(queryOptions = {}) {
  return useQuery(['ai-support', 'alerts'], listAlerts, { staleTime: 1000 * 20, ...queryOptions })
}

export function useCreateAlert() {
  const qc = useQueryClient()
  return useMutation((payload) => createAlert(payload), {
    onSuccess: () => qc.invalidateQueries(['ai-support', 'alerts']),
  })
}

export function useDeleteAlert() {
  const qc = useQueryClient()
  return useMutation((id) => deleteAlert(id), {
    onMutate: async (id) => {
      await qc.cancelQueries(['ai-support', 'alerts'])
      const previous = qc.getQueryData(['ai-support', 'alerts'])
      qc.setQueryData(['ai-support', 'alerts'], (old = []) => (old || []).filter((a) => a.id !== id))
      return { previous }
    },
    onError: (err, id, context) => qc.setQueryData(['ai-support', 'alerts'], context.previous),
    onSettled: () => qc.invalidateQueries(['ai-support', 'alerts']),
  })
}
