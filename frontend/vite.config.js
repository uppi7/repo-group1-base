import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  base: '/base/',   // 大盘 Nginx 挂载子路径，必须是顶层配置
  server: {
    host: '0.0.0.0',   // Docker 容器内必须监听 0.0.0.0，否则宿主机无法访问
    port: 5173,
    proxy: {
      //   proxy target 通过环境变量注入：
      //   本地直接运行: VITE_BACKEND_URL 未设置 → 回退 http://127.0.0.1:8081
      //   Docker dev:   VITE_BACKEND_URL=http://backend-base-dev:8081（service name）
      '/api/base': {
        target: process.env.VITE_BACKEND_URL || 'http://127.0.0.1:8081',
        changeOrigin: true,
      }
    }
  },
  build: {
    outDir: 'dist',
  }
})
