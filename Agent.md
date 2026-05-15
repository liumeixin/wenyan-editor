# Wenyan Editor — Agent Context

> 本文件由 Hermes Agent 维护，记录项目架构、决策和进展。人不要手动改。

## 项目定位

微信公众号 Markdown 排版工具。核心能力：Markdown → 带主题样式的 HTML → 复制到微信公众号编辑器。

## 架构决策

### 前后端分离

- `frontend/`：纯前端，standalone.html 可独立运行（唯一外部依赖 marked.js CDN）
- `backend/`：Flask API 服务，提供 Markdown 解析、主题 CSS 文件服务
- 前端通过 `fetch('themes.json')` 等相对路径加载数据，standalone 版本内联了所有数据

### 两种使用模式

1. **standalone.html**（推荐）：双击即用，无后端，所有 CSS 数据内联
2. **Flask 后端**：`backend/app.py` 提供 `/convert`、`/convert-inline` 等 API，适合需要内联样式输出的场景

### 构建流水线

```
CSS 源文件 (xhs-css-extract/)
  ↓ build.py
themes.json + dimensions.json + manifest.json
  ↓ build-static.py
standalone.html
```

## 文件说明

| 文件 | 用途 |
|------|------|
| `frontend/index.html` | 编辑器主页面（Flask 模板） |
| `frontend/standalone.html` | 独立版（274KB，数据内联） |
| `frontend/themes.json` | 15 个主题的完整 CSS（132KB） |
| `frontend/dimensions.json` | 18 个维度的混搭 CSS 片段（117KB） |
| `frontend/build.py` | 从 CSS 源文件构建 JSON（依赖外部 CSS 目录） |
| `frontend/build-static.py` | 从 index.html + JSON 构建 standalone |
| `backend/app.py` | Flask 服务（API + 前端托管） |
| `backend/markdown_parser.py` | 正则 Markdown 解析器（供 API 使用） |
| `backend/static/css/themes/` | 15 个主题 CSS 文件（供 `/api/theme-css/` 使用） |

## 技术约定

- CSS 主题数据统一用 JSON 格式，key 是主题 ID
- 维度数据按维度 key → 主题 → CSS 片段组织
- standalone 构建：替换 fetch 调用为内联 const 声明
- Flask 模板路径：`../frontend`（相对 backend/）

## 已知问题

- `build.py` 的 `CSS_DIR` 硬编码为 `/opt/data/cache/documents/xhs-css-extract`，只在 NAS 上可用
- `markdown_parser.py` 是正则实现，功能有限（不支持嵌套列表、复杂表格等），standalone 版用 marked.js 更强
- standalone 版的 marked.js 依赖 CDN，离线不可用

## 变更日志

### 2026-05-15：项目整合

- 将 wechat-md-styler（旧项目）和 wenyan-editor（新项目）合并为单一项目
- 清理旧项目废弃文件：wechat_styler.py、旧 templates/、旧 themes.json 等
- 更新 app.py 路径引用，模板从 `../frontend` 加载
- 构建脚本改为相对路径（`Path(__file__).parent`）
- Dockerfile 移至根目录，同时构建 frontend + backend
