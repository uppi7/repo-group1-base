# repo-group1-base/Makefile
IMAGE_BACKEND  = zjuse-backend-base
IMAGE_FRONTEND = zjuse-frontend-base
TAG            = latest

.PHONY: dev dev-d logs down build build-backend build-frontend clean

# ---- 本地开发（前台，含完整日志）----
dev:
	docker compose -f docker-compose.dev.yml --env-file .env up

# ---- 本地开发（后台）----
dev-d:
	docker compose -f docker-compose.dev.yml --env-file .env up -d

# ---- 停止开发环境 ----
down:
	docker compose -f docker-compose.dev.yml down

# ---- 构建后端生产镜像 ----
build-backend:
	docker build -t $(IMAGE_BACKEND):$(TAG) ./backend

# ---- 构建前端生产镜像（多阶段）----
build-frontend:
	docker build -t $(IMAGE_FRONTEND):$(TAG) ./frontend
	docker run --rm $(IMAGE_FRONTEND):$(TAG) ls /dist

build: build-backend build-frontend

# ---- 清理（含数据卷）----
clean:
	docker compose -f docker-compose.dev.yml down -v
