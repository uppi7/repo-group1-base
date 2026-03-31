<template>
  <div class="container">
    <h1>基础信息组 - 本地开发子系统</h1>
    <button @click="fetchTeacher" :disabled="loading">查询教师 #1001</button>

    <div v-if="loading" class="status">请求中...</div>
    <div v-if="result" class="result">
      <p>教师 ID：{{ result.id }}</p>
      <p>教师姓名：{{ result.name }}</p>
    </div>
    <div v-if="error" class="error">错误：{{ error }}</div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const loading = ref(false)
const result  = ref(null)
const error   = ref(null)

async function fetchTeacher() {
  loading.value = true
  result.value  = null
  error.value   = null
  try {
    // 前端只写相对路径，不硬编码主机名或端口
    // 本地开发：Vite proxy 将此请求转发到 http://127.0.0.1:8081
    // 大盘合并：Nginx 将 /api/base/ 转发到 http://backend-base:8081/
    const res = await fetch('/api/base/teacher/1001')
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    result.value = await res.json()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.container { font-family: sans-serif; max-width: 480px; margin: 60px auto; text-align: center; }
button { padding: 10px 24px; font-size: 16px; cursor: pointer; }
.result { margin-top: 20px; background: #e8f5e9; padding: 16px; border-radius: 8px; }
.error  { margin-top: 20px; background: #ffebee; padding: 16px; border-radius: 8px; }
.status { margin-top: 20px; color: #888; }
</style>
