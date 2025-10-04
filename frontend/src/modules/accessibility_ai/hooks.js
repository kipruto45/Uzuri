import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  listAccessibilityFeatures,
  createAccessibilityFeature,
  toggleAccessibilityFeature,
} from "./api";

export const ACCESSIBILITY_KEY = ["accessibility", "features"];

export function useAccessibilityFeatures() {
  return useQuery(ACCESSIBILITY_KEY, listAccessibilityFeatures, {
    staleTime: 1000 * 60,
  });
}

export function useCreateFeature() {
  const qc = useQueryClient();
  return useMutation(createAccessibilityFeature, {
    onMutate: async (newFeature) => {
      await qc.cancelQueries(ACCESSIBILITY_KEY);
      const previous = qc.getQueryData(ACCESSIBILITY_KEY);
      qc.setQueryData(ACCESSIBILITY_KEY, (old = []) => [
        { id: "temp-" + Date.now(), ...newFeature },
        ...old,
      ]);
      return { previous };
    },
    onError: (_err, _newFeature, context) => {
      qc.setQueryData(ACCESSIBILITY_KEY, context.previous);
    },
    onSettled: () => {
      qc.invalidateQueries(ACCESSIBILITY_KEY);
    },
  });
}

export function useToggleFeature() {
  const qc = useQueryClient();
  return useMutation(
    ({ id, enabled }) => toggleAccessibilityFeature(id, { enabled }),
    {
      onMutate: async ({ id, enabled }) => {
        await qc.cancelQueries(ACCESSIBILITY_KEY);
        const previous = qc.getQueryData(ACCESSIBILITY_KEY);
        qc.setQueryData(ACCESSIBILITY_KEY, (old = []) =>
          old.map((f) => (f.id === id ? { ...f, enabled } : f)),
        );
        return { previous };
      },
      onError: (_err, _vars, context) => {
        qc.setQueryData(ACCESSIBILITY_KEY, context.previous);
      },
      onSettled: () => qc.invalidateQueries(ACCESSIBILITY_KEY),
    },
  );
}
