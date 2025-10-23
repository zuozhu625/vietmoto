import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import node from '@astrojs/node';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  output: 'hybrid',  // 混合模式：大部分静态 + 部分SSR
  adapter: node({
    mode: 'standalone'
  }),
  integrations: [react()],
  vite: {
    plugins: [tailwindcss()],
  },
  server: {
    host: '0.0.0.0',  // 监听所有网络接口，支持公网访问
    port: 4321
  }
});

