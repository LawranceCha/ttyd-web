#!/usr/bin/env python3
"""tmux 会话列表 API"""

import subprocess
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import os

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

class SessionAPI(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # 静默日志

    def do_GET(self):
        path = urlparse(self.path).path

        if path == '/sessions':
            self.get_sessions()
        elif path == '/health':
            self.send_json({'status': 'ok'})
        elif path.startswith('/static/'):
            self.serve_static(path[8:])  # 去掉 /static/ 前缀
        else:
            self.send_error(404)

    def serve_static(self, filepath):
        """服务静态文件"""
        fullpath = os.path.join(STATIC_DIR, filepath)
        if not os.path.isfile(fullpath):
            self.send_error(404)
            return

        # 检查路径是否在 STATIC_DIR 内（安全检查）
        if not os.path.abspath(fullpath).startswith(STATIC_DIR):
            self.send_error(403)
            return

        # MIME 类型
        ext = os.path.splitext(filepath)[1]
        mimes = {'.js': 'application/javascript', '.css': 'text/css'}
        mime = mimes.get(ext, 'application/octet-stream')

        try:
            with open(fullpath, 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', mime)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500)

    def do_DELETE(self):
        path = urlparse(self.path).path
        if path.startswith('/session/'):
            name = path[9:]  # 去掉 '/session/'
            self.delete_session(name)
        else:
            self.send_error(404)

    def get_sessions(self):
        try:
            # 获取会话基本信息
            result = subprocess.run(
                ['tmux', 'list-sessions', '-F', '#{session_name}|#{session_windows}|#{session_created}'],
                capture_output=True, text=True, timeout=5
            )

            sessions = []
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        parts = line.split('|')
                        if len(parts) >= 2:
                            session_name = parts[0]
                            # 获取该会话第一个窗口的工作目录
                            cwd = self.get_session_cwd(session_name)
                            sessions.append({
                                'name': session_name,
                                'windows': int(parts[1]) if parts[1].isdigit() else 1,
                                'created': int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0,
                                'cwd': cwd
                            })

            self.send_json({'sessions': sessions})
        except Exception as e:
            self.send_json({'sessions': [], 'error': str(e)})

    def get_session_cwd(self, session_name):
        """获取会话的工作目录"""
        try:
            result = subprocess.run(
                ['tmux', 'list-panes', '-t', session_name, '-F', '#{pane_current_path}'],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                # 取第一个面板的工作目录
                paths = result.stdout.strip().split('\n')
                if paths:
                    # 缩短 home 目录
                    path = paths[0]
                    if path.startswith('/home/'):
                        parts = path.split('/')
                        if len(parts) >= 3:
                            path = '~' + path[5 + len(parts[1]):]
                    return path
        except:
            pass
        return '-'

    def delete_session(self, name):
        try:
            result = subprocess.run(
                ['tmux', 'kill-session', '-t', name],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                self.send_json({'success': True})
            else:
                self.send_json({'success': False, 'error': result.stderr})
        except Exception as e:
            self.send_json({'success': False, 'error': str(e)})

    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

if __name__ == '__main__':
    port = int(os.environ.get('API_PORT', 7682))
    server = HTTPServer(('0.0.0.0', port), SessionAPI)
    print(f"Session API running on port {port}")
    server.serve_forever()
