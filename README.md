# 文颜 Markdown 编辑器 (Wenyan Editor)

微信公众号 Markdown 排版工具，支持 15+ 主题 × 18 个维度的 CSS 混搭，轻松生成精美的公众号文章排版。

## ✨ 功能特色

- **15+ 主题**：涵盖文艺、科技、商务等多种风格
- **18 维度混搭**：字体、颜色、间距、边框等维度自由组合
- **手机预览模式**：实时模拟手机端阅读效果
- **XHS 小红书分页**：支持小红书风格的内容分页展示
- **独立模式**：无需后端服务，双击即可使用

## 📦 项目结构

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
├── wenyan-data/            # 主题配置数据
│   └── custom_themes.json  # 自定义主题配置
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## 🚀 使用方式

### 方式一：独立版（推荐）

直接在浏览器打开 `frontend/standalone.html`，所有功能本地运行。

- 无需安装任何依赖
- 唯一外部依赖：marked.js CDN（需联网解析 Markdown）
- 双击即用，适合快速体验和离线使用

### 方式二：Docker 部署

```bash
docker compose up -d
# 访问 http://localhost:18888
```

### 方式三：Flask 后端

```bash
pip install flask
cd backend
python app.py
# 访问 http://localhost:8080
```

## 🎨 自定义主题

编辑 `wenyan-data/custom_themes.json` 添加自定义主题配置。

## 🔧 开发指南

修改主题 CSS 后需要重新构建：

```bash
cd frontend
python build.py           # 从 CSS 源文件更新 themes.json / dimensions.json
python build-static.py    # 重新生成 standalone.html
```

`build.py` 支持通过环境变量 `WENYAN_CSS_DIR` 自定义 CSS 源文件目录：

```bash
WENYAN_CSS_DIR=/path/to/css python build.py
```

## 📄 License

MIT License
