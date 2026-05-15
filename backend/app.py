#!/usr/bin/env python3
"""
文颜 Markdown 排版器 — Flask Web 应用
====================================
支持一键换肤 + 单元素混搭

用法: python app.py
访问: http://localhost:8080
"""

import os
import json
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory, send_file

# --- Paths ---
BACKEND_DIR = Path(__file__).parent
FRONTEND_DIR = BACKEND_DIR / '..' / 'frontend'
THEMES_DIR = BACKEND_DIR / "static" / "css" / "themes"
CUSTOM_THEMES_FILE = Path(os.environ.get("DATA_DIR", str(BACKEND_DIR))) / "custom_themes.json"

app = Flask(__name__, template_folder=str(FRONTEND_DIR))


def _load_custom_themes():
    """读取自定义主题"""
    if CUSTOM_THEMES_FILE.exists():
        with open(CUSTOM_THEMES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def _save_custom_themes(themes):
    """保存自定义主题"""
    with open(CUSTOM_THEMES_FILE, 'w', encoding='utf-8') as f:
        json.dump(themes, f, ensure_ascii=False, indent=2)


# 解除图片加载限制
@app.after_request
def after_request(response):
    response.headers['Content-Security-Policy'] = "img-src * data: blob:;"
    return response


@app.route('/')
def index():
    """主页"""
    return send_file(FRONTEND_DIR / 'index.html')


@app.route('/convert', methods=['POST'])
def convert():
    """转换 Markdown 为 HTML"""
    try:
        data = request.get_json()
        markdown = data.get('markdown', '')

        if not markdown:
            return jsonify({'success': False, 'error': '输入为空'})

        from markdown_parser import parse_markdown
        html = parse_markdown(markdown)

        return jsonify({'success': True, 'html': html})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/convert-inline', methods=['POST'])
def convert_inline():
    """转换为微信公众号内联样式 HTML"""
    try:
        data = request.get_json()
        markdown = data.get('markdown', '')

        if not markdown:
            return jsonify({'success': False, 'error': '输入为空'})

        from markdown_parser import parse_markdown_for_wechat
        html = parse_markdown_for_wechat(markdown)

        return jsonify({'success': True, 'html': html})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/themes')
def api_themes():
    """返回主题列表"""
    themes_path = FRONTEND_DIR / "themes.json"
    with open(themes_path, 'r', encoding='utf-8') as f:
        themes = json.load(f)
        theme_index = [{"id": name, "name": name} for name in sorted(themes.keys())]
        return jsonify(theme_index)


@app.route('/api/dimensions')
def api_dimensions():
    """返回维度配置（用于混搭面板）"""
    config_path = FRONTEND_DIR / "dimensions.json"
    with open(config_path, 'r', encoding='utf-8') as f:
        return jsonify(json.load(f))


@app.route('/api/theme-css/<theme_id>')
def api_theme_css(theme_id):
    """返回指定主题的 CSS"""
    css_path = THEMES_DIR / f"{theme_id}.css"
    if css_path.exists():
        return send_from_directory(THEMES_DIR, f"{theme_id}.css", mimetype='text/css')
    return "Not found", 404


@app.route('/api/custom-themes', methods=['GET'])
def api_get_custom_themes():
    """获取所有自定义主题"""
    return jsonify(_load_custom_themes())


@app.route('/api/custom-themes', methods=['POST'])
def api_save_custom_theme():
    """保存自定义主题"""
    data = request.get_json()
    theme_id = data.get('id')
    theme_data = data.get('theme')
    if not theme_id or not theme_data:
        return jsonify({'success': False, 'error': '缺少 id 或 theme 数据'}), 400

    themes = _load_custom_themes()
    themes[theme_id] = theme_data
    _save_custom_themes(themes)
    return jsonify({'success': True})


@app.route('/api/custom-themes/<theme_id>', methods=['DELETE'])
def api_delete_custom_theme(theme_id):
    """删除自定义主题"""
    themes = _load_custom_themes()
    if theme_id in themes:
        del themes[theme_id]
        _save_custom_themes(themes)
    return jsonify({'success': True})


@app.route('/<path:filename>')
def serve_frontend(filename):
    """Serves frontend static files (themes.json, dimensions.json, etc.)"""
    file_path = FRONTEND_DIR / filename
    if file_path.exists() and file_path.is_file():
        return send_file(file_path)
    return "Not found", 404


def main():
    port = int(os.environ.get('PORT', 8080))
    host = os.environ.get('HOST', '0.0.0.0')

    print(f"""
╔══════════════════════════════════════════════════╗
║  文颜 Markdown 排版器                              ║
║  访问地址: http://localhost:{port:<20}║
╚══════════════════════════════════════════════════╝
""")

    app.run(host=host, port=port, debug=False)


if __name__ == '__main__':
    main()
