import os
import time
import pymysql
from flask import Flask, jsonify

app = Flask(__name__)

# 环境变量读取
DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
DB_PORT = int(os.environ.get("DB_PORT", "3306"))
DB_USER = os.environ.get("DB_USER", "root")
DB_PASS = os.environ.get("DB_PASS", "")
DB_NAME = os.environ.get("DB_NAME", "db_base")

# 本地开发时为 "true"（由 docker-compose.dev.yml 注入），生产镜像默认 false
FLASK_DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"


def get_conn():
    """带重试逻辑的数据库连接，应对容器启动竞态"""
    max_retries = 10
    for attempt in range(max_retries):
        try:
            return pymysql.connect(
                host=DB_HOST, port=DB_PORT, user=DB_USER,
                password=DB_PASS, database=DB_NAME,
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor,
                connect_timeout=5,
            )
        except pymysql.OperationalError as e:
            if attempt < max_retries - 1:
                print(f"[DB] 连接失败 ({attempt + 1}/{max_retries}): {e}，3s 后重试...")
                time.sleep(3)
            else:
                raise

# 这里为了简化用代码初始化，实际中可以写成init.sql
def init_db():
    conn = get_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS teacher (
                    id   INT PRIMARY KEY,
                    name VARCHAR(64) NOT NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            cur.execute("INSERT IGNORE INTO teacher (id, name) VALUES (1001, '张三')")
        conn.commit()
    print("[DB] 初始化完成")


@app.route("/api/base/teacher/<int:teacher_id>")
def get_teacher(teacher_id):
    conn = get_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name FROM teacher WHERE id = %s", (teacher_id,))
            row = cur.fetchone()
    if row is None:
        return jsonify({"error": "teacher not found"}), 404
    return jsonify({"id": row["id"], "name": row["name"]})


@app.route("/api/base/health")
def health():
    return jsonify({"status": "ok", "service": "backend-base"})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8081, debug=FLASK_DEBUG)
    # FLASK_DEBUG=true 时 Flask Reloader 监听文件变更自动重启，配合 volume mount 实现热重载
