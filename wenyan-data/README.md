# 文言 Markdown 排版器

一键换肤 · 元素混搭 · 微信公众号/小红书排版工具

## 功能

- **15 个内置主题**：默认黑白、赛博朋克、烟花夜、马卡龙等
- **10 维度混搭**：背景、正文、标题、引用块、代码块、链接、表格、分割线、图片、强调
- **自定义主题**：混搭组合可保存命名，服务端持久化存储
- **微信公众号复制**：一键复制内联样式 HTML，粘贴到公众号后台即用
- **实时预览**：Markdown 输入即时渲染

## 快速开始

### Docker 部署（推荐）

```bash
git clone https://github.com/liumeixin/wenyan-editor.git
cd wenyan-editor/wenyan-data
docker compose up -d
```

访问 `http://localhost:18080`

### 本地运行

```bash
pip install flask
python app.py
```

访问 `http://localhost:8080`

## 端口说明

| 端口 | 说明 |
|------|------|
| 8080 | 容器内部 Flask 监听端口 |
| 18080 | 宿主机映射端口（可通过 docker-compose.yml 修改） |

## 目录结构

```
wenyan-data/
├── app.py                  # Flask 后端
├── markdown_parser.py      # Markdown 解析器
├── custom_themes.json      # 自定义主题持久化存储
├── templates_flask/
│   └── index.html          # 前端 UI
├── static/
│   ├── themes_index.json   # 主题列表索引
│   ├── dimensions_config.json  # 维度混搭配置
│   └── css/
│       ├── base.css        # CSS 变量体系
│       └── themes/         # 15 个主题 CSS 文件
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## API

| 接口 | 方法 | 说明 |
|------|------|------|
| `/convert` | POST | Markdown → 语义化 HTML（预览用） |
| `/convert-inline` | POST | Markdown → 内联样式 HTML（公众号用） |
| `/api/themes` | GET | 内置主题列表 |
| `/api/dimensions` | GET | 维度混搭配置 |
| `/api/theme-css/<id>` | GET | 主题 CSS 文件 |
| `/api/custom-themes` | GET/POST | 自定义主题增查改 |
| `/api/custom-themes/<id>` | DELETE | 删除自定义主题 |

## 自定义主题

混搭面板中组合不同维度的风格后，点击「💾 保存为自定义主题」，输入名称即可保存。数据存储在 `custom_themes.json`，清浏览器数据不丢失。

## 后续开发

修改代码后只需重启容器，无需重建镜像：

```bash
docker restart wenyan
```
