import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  listNotifications,
  listUnreadCount,
  markRead,
} from "../services/notifications";

export function useNotifications(limit = 10, opts = {}) {
  return useQuery(
    ["notifications", { limit }],
    () => listNotifications({ limit }),
    {
      staleTime: 1000 * 20,
      refetchInterval: opts.pollInterval || 30000,
    },
  );
}

export function useUnreadCount() {
  return useQuery(["notifications", "unread_count"], listUnreadCount, {
    staleTime: 1000 * 20,
  });
}

export function useMarkRead() {
  const qc = useQueryClient();
  return useMutation((id) => markRead(id), {
    onSuccess: () => {
      qc.invalidateQueries(["notifications"]);
      qc.invalidateQueries(["notifications", "unread_count"]);
    },
  });
}
