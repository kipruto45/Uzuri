// Global Jest setup: ensure QueryClient has defaultMutationOptions used by useMutation
try {
  const { QueryClient } = require('@tanstack/react-query')
  if (QueryClient && typeof QueryClient.prototype.defaultMutationOptions !== 'function') {
    // eslint-disable-next-line no-extend-native
    QueryClient.prototype.defaultMutationOptions = function (opts) { return opts || {} }
  }
} catch (e) {
  // ignore if package not present
}
