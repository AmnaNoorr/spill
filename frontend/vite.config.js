import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/auth': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/markets': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/oracles': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/health': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/stats': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
    },
  },
})
