# 基础信息组（group1）

本仓库负责**教师/课程基础信息**的查询服务，是整个大系统的数据源头。

## 架构

```
frontend (Vue + Vite)  :5173
        ↓ proxy /api/base/*
backend (Flask)        :8081
        ↓
MySQL                  :3306   逻辑库 db_base
```

开发环境三个服务全部跑在 Docker 里，本机不需要安装 Python 或 Node。

---

## 快速开始

### 1. 初始化配置

```bash
cp .env.example .env
# 用编辑器打开 .env，将 DB_PASS 改为任意本地密码（如 dev123）
```

`.env` 里只有本地开发用的密码，**不要提交到 Git**（已在 `.gitignore` 中）。

### 2. 启动开发环境

```bash
make dev
```

首次运行会拉取镜像、安装依赖，约需 2-3 分钟。看到以下输出说明就绪：

```
backend-base-dev  | [DB] 初始化完成
backend-base-dev  |  * Running on http://0.0.0.0:8081
frontend-base-dev |   ➜  Local: http://localhost:5173/
```

### 3. 验证

```bash
curl http://localhost:8081/api/base/health
curl http://localhost:8081/api/base/teacher/1001
```

浏览器访问 `http://localhost:5173`，点击「查询教师 #1001」。

### 4. 停止

```bash
make down
```

### 5. 清理

```bash
make clean
```
---

## 开发规范

### 环境变量读取

```python
# ✅ 正确
DB_PASS = os.environ.get("DB_PASS")

# ❌ 错误
DB_PASS = "dev123"
```

`docker-compose.dev.yml` 在启动时会把 `.env` 里的变量注入容器，大盘合并时由大组的 `infrastructure/.env` 统一注入。

### 前端只用相对路径

```javascript
// ✅ 正确——本地由 Vite proxy 转发，合并后由 Nginx 转发
const res = await fetch('/api/base/teacher/1001')

// ❌ 错误
const res = await fetch('http://localhost:8081/api/base/teacher/1001')
```

### 数据库连接要有重试

MySQL 容器启动后约需 15 秒才 ready，`app.py` 已内置重试逻辑。

---

## 交付物

每次推送 `main` 分支，GitHub Actions 自动构建两个镜像推送到 ghcr.io：

| 镜像 | 说明 |
|------|------|
| `ghcr.io/uppi7/zjuse-backend-base:latest` | Flask 服务，有启动进程 |
| `ghcr.io/uppi7/zjuse-frontend-base:latest` | 仅含 `/dist` 静态文件，无启动进程 |


---

## 提交前自查

```
[ ] 新增的环境变量已同步到 .env.example
[ ] 前端 fetch 全部使用相对路径
等等..
```
