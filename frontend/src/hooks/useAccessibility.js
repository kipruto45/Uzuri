import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { listAccessibilityFeatures, toggleAccessibilityFeature, createAccessibilityFeature, deleteAccessibilityFeature } from '../modules/accessibility_ai/api'

export function useAccessibilityFeatures() {
  return useQuery(['accessibility', 'features'], listAccessibilityFeatures, { staleTime: 1000 * 30 })
}

export function useToggleFeature() {
  const qc = useQueryClient()
  return useMutation(({ id, enabled }) => toggleAccessibilityFeature(id, { enabled }), {
    onMutate: async ({ id, enabled }) => {
      await qc.cancelQueries(['accessibility', 'features'])
      const previous = qc.getQueryData(['accessibility', 'features'])
      qc.setQueryData(['accessibility', 'features'], (old) => old.map((f) => (f.id === id ? { ...f, enabled } : f)))
      return { previous }
    },
    onError: (err, variables, context) => qc.setQueryData(['accessibility', 'features'], context.previous),
    onSettled: () => qc.invalidateQueries(['accessibility', 'features']),
  })
}

export function useCreateFeature() {
  const qc = useQueryClient()
  return useMutation((payload) => createAccessibilityFeature(payload), {
    onSuccess: () => qc.invalidateQueries(['accessibility', 'features']),
  })
}

export function useDeleteFeature() {
  const qc = useQueryClient()
  return useMutation((id) => deleteAccessibilityFeature(id), {
    onSuccess: () => qc.invalidateQueries(['accessibility', 'features']),
  })
}
