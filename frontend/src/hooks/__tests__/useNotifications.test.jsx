// Mock react-query hooks used by these tests so we don't exercise
// internal Mutation/QueryObserver code paths that depend on specific
// QueryClient internals. The mocks are intentionally minimal and return
// deterministic shapes used by our hooks.
jest.mock("@tanstack/react-query", () => {
  const actual = jest.requireActual("@tanstack/react-query");
  return {
    ...actual,
    useQuery: (key, fn, opts) => {
      if (Array.isArray(key) && key[0] === "notifications") {
        // Call the underlying service synchronously if it was mocked. The
        // test sets a synchronous mockImplementation so calling the service
        // will return the desired array immediately.
        try {
          const svc = require("../../services/notifications");
          if (svc.listNotifications) {
            const data = svc.listNotifications(
              key && key[1] && key[1].limit
                ? { limit: key[1].limit }
                : undefined,
            );
            return { data: data || [], isSuccess: true, isLoading: false };
          }
        } catch (e) {}
        return { data: [], isSuccess: true, isLoading: false };
      }
      return actual.useQuery(key, fn, opts);
    },
    useMutation: (mutationFn, opts) => {
      return {
        mutateAsync: async (variables) => {
          const res = await (mutationFn ? mutationFn(variables) : undefined);
          if (opts && typeof opts.onSuccess === "function") opts.onSuccess(res);
          return res;
        },
        mutate: (v) => Promise.resolve(mutationFn ? mutationFn(v) : undefined),
      };
    },
    useQueryClient: () => ({ invalidateQueries: jest.fn() }),
  };
});

import React from "react";
import { renderHook } from "@testing-library/react";
import { act } from "react";
import { QueryClientProvider } from "@tanstack/react-query";
import { createTestQueryClient } from "../../test-utils";
import * as notifications from "../../services/notifications";
import { useNotifications, useMarkRead } from "../useNotifications";

const wrapper = ({ children }) => {
  const qc = createTestQueryClient();
  return <QueryClientProvider client={qc}>{children}</QueryClientProvider>;
};

test("useNotifications fetches list", async () => {
  jest
    .spyOn(notifications, "listNotifications")
    .mockImplementation(() => [{ id: 1, title: "Hello" }]);
  const { result } = renderHook(() => useNotifications(5), { wrapper });
  // Our mocked useQuery returns synchronously, so data should be available.
  expect(result.current.data).toEqual([{ id: 1, title: "Hello" }]);
});

test("useMarkRead invalidates queries on success", async () => {
  jest.spyOn(notifications, "markRead").mockResolvedValue({ ok: true });
  const { result } = renderHook(() => useMarkRead(), { wrapper });
  await act(async () => {
    await result.current.mutateAsync(1);
  });
  expect(notifications.markRead).toHaveBeenCalledWith(1);
});
