import { useEffect, useRef } from "react";
import { useDispatch } from "react-redux";
import { pushNotification } from "../store/slices/notificationsSlice";

// url should be like ws://localhost:8000/ws/notifications/
export default function useWebSocket(url, { autoReconnect = true } = {}) {
  const wsRef = useRef(null);
  const dispatch = useDispatch();

  useEffect(() => {
    if (!url) return;

    let mounted = true;

    function connect() {
      const ws = new WebSocket(url);
      wsRef.current = ws;

      ws.onopen = () => {
        console.log("ws open", url);
      };

      ws.onmessage = (evt) => {
        try {
          const data = JSON.parse(evt.data);
          // Dispatch a notification action if payload has type 'notification'
          if (data.type === "notification" || data.event === "notification") {
            dispatch(pushNotification(data));
          }
        } catch (e) {
          console.log("ws message", evt.data);
        }
      };

      ws.onclose = () => {
        console.log("ws closed", url);
        if (autoReconnect && mounted) {
          setTimeout(connect, 2000);
        }
      };

      ws.onerror = (err) => {
        console.error("ws error", err);
        ws.close();
      };
    }

    connect();

    return () => {
      mounted = false;
      if (wsRef.current) wsRef.current.close();
    };
  }, [url, autoReconnect, dispatch]);

  return wsRef;
}
