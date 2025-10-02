import React from 'react'
import { render } from '@testing-library/react'

const { QueryClient, QueryClientProvider } = require('@tanstack/react-query')
// Also attempt to shim the QueryClient from query-core in case the runtime
// loads a separate copy (some installations include both packages separately).
let QueryCoreClient = null
try {
  QueryCoreClient = require('@tanstack/query-core').QueryClient
} catch (e) {
  // ignore if not present
}

export function renderWithClient(ui, { queryClientOptions, ...renderOptions } = {}) {
  // Ensure the QueryClient prototype exposes defaultMutationOptions for older/newer react-query combos
  if (typeof QueryClient.prototype.defaultMutationOptions !== 'function') {
    // eslint-disable-next-line no-extend-native
    QueryClient.prototype.defaultMutationOptions = function () { return {} }
  }
  if (QueryCoreClient && typeof QueryCoreClient.prototype.defaultMutationOptions !== 'function') {
    // eslint-disable-next-line no-extend-native
    QueryCoreClient.prototype.defaultMutationOptions = function () { return {} }
  }

  const client = new QueryClient({ defaultOptions: { queries: { retry: false } }, ...(queryClientOptions || {}) })

  // Some react-query versions access defaultMutationOptions directly on the client instance.
  // Ensure the instance has the method as a safety shim for tests.
  // eslint-disable-next-line no-param-reassign
  if (typeof client.defaultMutationOptions !== 'function') {
    client.defaultMutationOptions = function () { return {} }
  }
  // If query-core exports a separate QueryClient class and the test runtime ends up
  // using a client instance from that class, ensure any such instance also has the method.
  if (QueryCoreClient && client instanceof QueryCoreClient && typeof client.defaultMutationOptions !== 'function') {
    client.defaultMutationOptions = function () { return {} }
  }

  function Wrapper({ children }) {
    return <QueryClientProvider client={client}>{children}</QueryClientProvider>
  }

  return render(ui, { wrapper: Wrapper, ...renderOptions })
}

export * from '@testing-library/react'
export { default as userEvent } from '@testing-library/user-event'
