#!/bin/bash
# ttyd 服务启动脚本

# 停止旧进程
pkill -f "session-api.py" 2>/dev/null || true
pkill -f "ttyd.*7681" 2>/dev/null || true
sleep 1

# 启动会话 API
cd /home/cha/ttyd-web
python3 session-api.py &
sleep 1

# 启动 ttyd
exec ttyd --port 7681 --interface 0.0.0.0 --writable --index /home/cha/ttyd-web/index.html --terminal-type xterm-256color bash
