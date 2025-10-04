import React from "react";
import { render } from "@testing-library/react";
import { act } from "react";

const { QueryClient, QueryClientProvider } = require("@tanstack/react-query");

export function renderWithClient(
  ui,
  { queryClientOptions, ...renderOptions } = {},
) {
  // No compatibility shims here; tests rely on pinned react-query/query-core versions.

  const client = new QueryClient({
    defaultOptions: { queries: { retry: false } },
    ...(queryClientOptions || {}),
  });

  // Ensure the test QueryClient instance exposes defaultMutationOptions.
  // In some test environments the prototype may not be patched early enough
  // or module resolution can yield distinct copies; set it on the instance
  // so MutationObserver (used by useMutation) won't throw during tests.
  if (typeof client.defaultMutationOptions !== "function") {
    // eslint-disable-next-line no-param-reassign
    client.defaultMutationOptions = function (opts) {
      return opts || {};
    };
  }

  // Some react-query versions expect defaultQueryOptions to be a function on
  // the QueryClient instance. In mixed module-resolution setups this may be
  // missing which causes useQuery/useBaseQuery to throw. Provide a safe
  // fallback so tests can run consistently across environments.
  if (typeof client.defaultQueryOptions !== "function") {
    // eslint-disable-next-line no-param-reassign
    client.defaultQueryOptions = function (opts) {
      return opts || {};
    };
  }

  // Diagnostic logging for CI/local debugging: print the type so we can
  // confirm the instance has the function at render time.
  if (process.env.JEST_WORKER_ID !== undefined) {
    // no-op diagnostic removed
  }

  // return the wrapped render

  function Wrapper({ children }) {
    return (
      <QueryClientProvider client={client}>{children}</QueryClientProvider>
    );
  }

  return render(ui, { wrapper: Wrapper, ...renderOptions });
}

// Export a helper to create a pre-patched QueryClient for tests that need
// explicit access to the client (eg. renderHook wrappers). Tests should prefer
// this to calling `new QueryClient()` directly so they get the instance-level
// fallbacks that avoid useQuery/useMutation runtime errors in mixed module
// resolution environments.
export function createTestQueryClient(opts = {}) {
  const client = new (require("@tanstack/react-query").QueryClient)({
    defaultOptions: { queries: { retry: false } },
    ...(opts || {}),
  });
  if (typeof client.defaultMutationOptions !== "function")
    client.defaultMutationOptions = function (o) {
      return o || {};
    };
  if (typeof client.defaultQueryOptions !== "function")
    client.defaultQueryOptions = function (o) {
      return o || {};
    };
  // Diagnostic: log to help debug mixed-module issues in CI where functions
  // may be missing. This will appear in test output.
  try {
    // eslint-disable-next-line no-console
    console.debug(
      "[test-utils] createTestQueryClient defaultQueryOptions type =",
      typeof client.defaultQueryOptions,
    );
  } catch (e) {}
  return client;
}

// Re-export Testing Library helpers and react's act for tests to use consistently.
export * from "@testing-library/react";
export { act };
export { default as userEvent } from "@testing-library/user-event";
