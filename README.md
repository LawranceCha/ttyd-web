# ttyd-web

Mac 风格 Web 终端 - 基于 ttyd 和 xterm.js 的现代化终端界面

## 功能特点

- **Mac 风格窗口外观** - 红黄绿按钮、圆角窗口、毛玻璃效果
- **快捷按钮栏** - 返回、主目录、列表、tmux 操作等常用命令
- **历史命令面板** - Ctrl+R 搜索，快速执行历史命令
- **多主题支持** - Default、Dracula、Monokai、Solarized Dark、Nord
- **会话管理** - 自动启动 tmux 会话，支持多会话切换
- **自定义字体** - 支持选择字体和大小调整

## 技术栈

- [ttyd](https://github.com/tsl0922/ttyd) - Web 终端后端
- [xterm.js](https://xtermjs.org/) - 终端模拟器
- [tmux](https://github.com/tmux/tmux) - 会话管理
- Python 3 - 会话 API 服务

## 安装依赖

```bash
# Ubuntu/Debian
sudo apt install ttyd tmux

# Arch Linux
sudo pacman -S ttyd tmux
```

## 快速开始

```bash
# 克隆项目
git clone https://github.com/LawranceCha/ttyd-web.git
cd ttyd-web

# 启动服务
./start.sh

# 访问
# http://localhost:7681
```

## 配置

环境变量：

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `PORT` | 7681 | ttyd 服务端口 |
| `API_PORT` | 7682 | 会话 API 端口 |

## 快捷键

- `Ctrl + R` - 搜索历史命令
- `Ctrl + Shift + C` - 复制选中内容
- `Ctrl + Shift + V` - 粘贴
- `Shift + 拖动` - 框选文本

## 项目结构

```
ttyd-web/
├── index.html        # 主页面（包含 HTML/CSS/JS）
├── start.sh          # 启动脚本
├── session-api.py    # tmux 会话管理 API
├── static/           # 静态资源
│   ├── css/          # 样式文件
│   └── js/           # JavaScript 文件
└── .gitignore
```

## 截图

会话选择界面和终端界面均采用深色主题，具有现代化的 UI 设计。

## 许可证

MIT License
