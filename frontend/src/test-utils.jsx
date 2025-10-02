import React from 'react'
import { render } from '@testing-library/react'

const { QueryClient, QueryClientProvider } = require('@tanstack/react-query')

export function renderWithClient(ui, { queryClientOptions, ...renderOptions } = {}) {
  // No compatibility shims here; tests rely on pinned react-query/query-core versions.

  const client = new QueryClient({ defaultOptions: { queries: { retry: false } }, ...(queryClientOptions || {}) })

  // Ensure the test QueryClient instance exposes defaultMutationOptions.
  // In some test environments the prototype may not be patched early enough
  // or module resolution can yield distinct copies; set it on the instance
  // so MutationObserver (used by useMutation) won't throw during tests.
  if (typeof client.defaultMutationOptions !== 'function') {
    // eslint-disable-next-line no-param-reassign
    client.defaultMutationOptions = function (opts) { return opts || {} }
  }

  // Diagnostic logging for CI/local debugging: print the type so we can
  // confirm the instance has the function at render time.
  if (process.env.JEST_WORKER_ID !== undefined) {
    // eslint-disable-next-line no-console
    console.log('test-utils: defaultMutationOptions type=', typeof client.defaultMutationOptions)
  }

  // return the wrapped render

  function Wrapper({ children }) {
    return <QueryClientProvider client={client}>{children}</QueryClientProvider>
  }

  return render(ui, { wrapper: Wrapper, ...renderOptions })
}

export * from '@testing-library/react'
export { default as userEvent } from '@testing-library/user-event'
