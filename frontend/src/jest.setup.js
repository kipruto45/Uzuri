// Global Jest setup: ensure QueryClient has defaultMutationOptions used by useMutation
try {
  // Patch QueryClient from react-query if present
  try {
    const rq = require('@tanstack/react-query')
    if (rq && rq.QueryClient && typeof rq.QueryClient.prototype.defaultMutationOptions !== 'function') {
      // eslint-disable-next-line no-extend-native
      rq.QueryClient.prototype.defaultMutationOptions = function (opts) { return opts || {} }
    }
  } catch (e) {
    // ignore
  }
  // Patch QueryClient from query-core if present
  try {
    const qc = require('@tanstack/query-core')
    if (qc && qc.QueryClient && typeof qc.QueryClient.prototype.defaultMutationOptions !== 'function') {
      // eslint-disable-next-line no-extend-native
      qc.QueryClient.prototype.defaultMutationOptions = function (opts) { return opts || {} }
    }
  } catch (e) {
    // ignore
  }
} catch (e) {
  // ignore if package not present
}
