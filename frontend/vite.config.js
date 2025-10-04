import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // Proxy /api to Django backend running on localhost:8000
    proxy: {
      "/api": "http://localhost:8000",
      "/api/v1": "http://localhost:8000",
    },
  },
});
