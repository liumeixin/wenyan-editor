# 文颜 Markdown 编辑器 (Wenyan Editor)

微信公众号 Markdown 排版工具，支持 15 个主题 × 18 个维度的 CSS 混搭。

## 项目结构

```
wenyan-editor/
├── frontend/               # 前端
│   ├── index.html          # 编辑器页面（需配合后端）
│   ├── standalone.html     # 独立版（双击即用，无需后端）
│   ├── themes.json         # 主题 CSS 数据
│   ├── dimensions.json     # 维度混搭数据
│   ├── manifest.json       # 主题/维度索引
│   ├── build.py            # 从 CSS 源文件构建 JSON 数据
│   └── build-static.py     # 从 index.html 构建 standalone 版本
├── backend/                # 后端
│   ├── app.py              # Flask 服务（API + 静态文件）
│   ├── markdown_parser.py  # Markdown → HTML 解析器
│   └── static/css/themes/  # 15 个主题 CSS 文件
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## 使用方式

### 方式一：独立版（推荐，无需后端）

直接在浏览器打开 `frontend/standalone.html`，所有功能本地运行。
唯一外部依赖：marked.js CDN（需联网解析 Markdown）。

### 方式二：Flask 后端

```bash
# 本地运行
cd backend
pip install flask
python app.py
# 访问 http://localhost:8080

# Docker 运行
docker compose up -d
# 访问 http://localhost:18888
```

### 重新构建数据

修改主题 CSS 后需要重新构建：

```bash
cd frontend
python build.py           # 从 CSS 源文件更新 themes.json / dimensions.json
python build-static.py    # 重新生成 standalone.html
```

## 技术栈

- **前端**：HTML + CSS + vanilla JS（marked.js CDN）
- **后端**：Python Flask
- **部署**：Docker (python:3.11-slim)
