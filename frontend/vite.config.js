import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  root: '.',           // project root contains index.html
  publicDir: 'public', // static files
  plugins: [react()],
  server: {
    port: 3000,
    open: true
  }
});