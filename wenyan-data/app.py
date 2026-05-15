#!/usr/bin/env python3
"""
文言 Markdown 排版器 — Flask Web 应用
=====================================
支持一键换肤 + 单元素混搭 + 自定义主题持久化

用法: python app.py
访问: http://localhost:18080
"""

import os
import json
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__, template_folder='templates_flask')

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
THEMES_DIR = STATIC_DIR / "css" / "themes"
CUSTOM_THEMES_FILE = BASE_DIR / "custom_themes.json"


def _load_custom_themes():
    """读取自定义主题"""
    if CUSTOM_THEMES_FILE.exists():
        with open(CUSTOM_THEMES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def _save_custom_themes(themes):
    """保存自定义主题"""
    CUSTOM_THEMES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CUSTOM_THEMES_FILE, 'w', encoding='utf-8') as f:
        json.dump(themes, f, ensure_ascii=False, indent=2)


@app.after_request
def after_request(response):
    response.headers['Content-Security-Policy'] = "img-src * data: blob:;"
    return response


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/convert', methods=['POST'])
def convert():
    """转换 Markdown 为 HTML（预览用）"""
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
    """返回内置主题列表"""
    index_path = STATIC_DIR / "themes_index.json"
    with open(index_path, 'r', encoding='utf-8') as f:
        return jsonify(json.load(f))


@app.route('/api/dimensions')
def api_dimensions():
    """返回维度配置（混搭面板用）"""
    config_path = STATIC_DIR / "dimensions_config.json"
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
        return jsonify({'success': False, 'error': '缺少 id 或 theme'}), 400
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


def main():
    port = int(os.environ.get('PORT', 8080))
    host = os.environ.get('HOST', '0.0.0.0')
    print(f"\n  文言 Markdown 排版器\n  http://localhost:{port}\n")
    app.run(host=host, port=port, debug=False)


if __name__ == '__main__':
    main()
