// WebSocket helper that attaches a JWT access token as a query param
const DEFAULT_WS_PATH = () => {
  const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws'
  const host = window.location.host
  return `${protocol}://${host}/ws/notifications/`
}

export function createWebSocket(onMessage, onOpen, onClose) {
  let url = DEFAULT_WS_PATH()
  try {
    const raw = localStorage.getItem('uzuri_auth')
    if (raw) {
      const { access } = JSON.parse(raw)
      if (access) {
        const sep = url.includes('?') ? '&' : '?'
        url = `${url}${sep}token=${encodeURIComponent(access)}`
      }
    }
  } catch (e) {
    // ignore
  }

  const ws = new WebSocket(url)

  ws.onopen = (e) => onOpen && onOpen(e)
  ws.onmessage = (evt) => {
    try {
      const data = JSON.parse(evt.data)
      onMessage && onMessage(data)
    } catch (e) {
      onMessage && onMessage(evt.data)
    }
  }
  ws.onclose = (e) => onClose && onClose(e)

  return ws
}

export default { createWebSocket }
