import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      // Points at Yojit's FastAPI backend. Adjust host/port to match
      // whatever docker-compose / uvicorn ends up running on.
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      // Anwesha's image_analysis/app.py calls uvicorn.run() itself rather
      // than being mounted into main.py, so it's its own process on its
      // own port. Port below is a placeholder — ask her what it actually
      // runs on and update this.
      '/image-api': {
        target: 'http://localhost:8001',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/image-api/, '')
      }
    }
  }
})
