// Lightweight local fake for @tanstack/react-query to avoid test-time
// mixed-module QueryClient errors. It provides a tiny in-memory cache and
// mutation lifecycle used by our components.
jest.mock("@tanstack/react-query", () => {
  const store = new Map();
  const keyToStr = (k) => {
    try {
      return JSON.stringify(k);
    } catch (e) {
      return String(k);
    }
  };
  function useQuery(key, fn) {
    const k = keyToStr(key);
    if (store.has(k)) return { data: store.get(k), isLoading: false };
    try {
      const res = fn();
      if (res && typeof res.then === "function")
        return { data: undefined, isLoading: true };
      store.set(k, res);
      return { data: res, isLoading: false };
    } catch (e) {
      return { data: undefined, isLoading: false };
    }
  }
  function useQueryClient() {
    return {
      getQueryData: (key) => store.get(keyToStr(key)),
      setQueryData: (key, updater) => {
        const k = keyToStr(key);
        const old = store.has(k) ? store.get(k) : undefined;
        const next = typeof updater === "function" ? updater(old) : updater;
        store.set(k, next);
        return next;
      },
      cancelQueries: () => Promise.resolve(),
      invalidateQueries: () => Promise.resolve(),
    };
  }
  function useMutation(mutationFn, opts = {}) {
    async function mutate(variables) {
      let context;
      try {
        if (opts.onMutate) context = await opts.onMutate(variables);
        const res = await Promise.resolve(mutationFn(variables));
        if (opts.onSuccess) opts.onSuccess(res, variables, context);
        if (opts.onSettled) opts.onSettled(res, null, variables, context);
        return res;
      } catch (err) {
        if (opts.onError) opts.onError(err, variables, context);
        if (opts.onSettled) opts.onSettled(undefined, err, variables, context);
        throw err;
      }
    }
    return { mutate, mutateAsync: mutate };
  }
  function QueryClient() {}
  function QueryClientProvider({ children }) {
    return children;
  }
  return {
    useQuery,
    useMutation,
    useQueryClient,
    QueryClient,
    QueryClientProvider,
  };
});

import React from "react";
import { renderWithClient, userEvent, screen } from "../../../test-utils";
import AiSupportPage from "../AiSupportPage";
import * as api from "../api";

jest.mock("../api");

describe("AiSupportPage", () => {
  afterEach(() => jest.clearAllMocks());

  test("renders empty states and allows creating conversation, recommendation and alert", async () => {
    api.listConversations.mockReturnValue([]);
    api.listStudyRecommendations.mockReturnValue([]);
    api.listAlerts.mockReturnValue([]);

    api.createConversation.mockImplementation(() => ({
      id: 1,
      message: "hey",
      response: "hello",
    }));
    api.createStudyRecommendation.mockImplementation(() => ({
      id: 1,
      recommendation: "Study more",
    }));
    api.createAlert.mockImplementation(() => ({ id: 1, message: "Alert" }));

    renderWithClient(<AiSupportPage />);

    // empty states should appear
    expect(
      await screen.findByText(/No conversations yet/i),
    ).toBeInTheDocument();
    expect(
      await screen.findByText(/No recommendations yet/i),
    ).toBeInTheDocument();
    expect(await screen.findByText(/No alerts/i)).toBeInTheDocument();

    // create conversation
    const input = screen.getByLabelText(/message input/i);
    await userEvent.type(input, "hello");
    await userEvent.click(
      screen.getByRole("button", { name: /send message/i }),
    );
    expect(api.createConversation).toHaveBeenCalled();

    // create recommendation
    const recInput = screen.getByPlaceholderText(/Add recommendation/i);
    await userEvent.type(recInput, "Practice tests");
    await userEvent.click(screen.getByRole("button", { name: /add/i }));
    expect(api.createStudyRecommendation).toHaveBeenCalled();

    // create alert
    const alertInput = screen.getByPlaceholderText(/Create alert/i);
    await userEvent.type(alertInput, "System maintenance");
    await userEvent.click(screen.getByRole("button", { name: /create/i }));
    expect(api.createAlert).toHaveBeenCalled();
  });
});
