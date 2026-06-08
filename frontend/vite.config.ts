import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    // Proxy /api/* → http://localhost:8000/* during development.
    // The browser makes requests to localhost:5173/api/products, Vite forwards
    // them to localhost:8000/products. No CORS headers needed on the backend.
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        rewrite: path => path.replace(/^\/api/, ''),
      },
    },
  },
})
