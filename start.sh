#!/bin/bash
# ttyd + 会话 API 服务

PORT=${PORT:-7681}
API_PORT=${API_PORT:-7682}
INDEX_PATH="/home/cha/ttyd-web/index.html"

echo "==================================="
echo "  终端会话管理器"
echo "==================================="
echo "终端端口: $PORT"
echo "API 端口: $API_PORT"
echo "访问: http://localhost:$PORT"
echo "==================================="

# 停止旧进程
pkill -f "ttyd.*$PORT" 2>/dev/null
pkill -f "session-api.*$API_PORT" 2>/dev/null
sleep 1

# 启动会话 API
python3 /home/cha/ttyd-web/session-api.py &
sleep 1

# 启动 ttyd
ttyd \
    --port "$PORT" \
    --interface 0.0.0.0 \
    --writable \
    --index "$INDEX_PATH" \
    --terminal-type xterm-256color \
    bash
