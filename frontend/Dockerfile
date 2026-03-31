# 多阶段构建
# Stage 1: node 镜像负责编译，产出 dist/
FROM node:20-alpine AS builder

WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
RUN npm run build

# Stage 2: 轻量 alpine 镜像仅承载静态文件，无任何运行时进程
# 大盘 Nginx 使用 COPY --from=zjuse-frontend-base:latest /dist /usr/share/nginx/html/base 缝合
FROM alpine:3.19

WORKDIR /dist
# 将编译产物复制到 /dist，供大盘 gateway Dockerfile 隔空拉取
COPY --from=builder /app/dist /dist

# 无 CMD：此镜像仅作为静态文件载体，不启动任何进程
