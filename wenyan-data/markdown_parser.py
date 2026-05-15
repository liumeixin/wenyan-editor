#!/usr/bin/env python3
"""文言 Markdown 解析器 — MD → 语义化 HTML"""

import re


def parse_markdown(md: str) -> str:
    """将 Markdown 转换为语义化 HTML（预览用，CSS 控制样式）"""
    html = md

    # 去除 frontmatter
    html = re.sub(r'^---\n[\s\S]*?\n---\n', '', html)

    # 图片
    html = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1">', html)

    # 代码块
    html = re.sub(r'```(\w*)\n(.*?)```', r'<pre><code class="language-\1">\2</code></pre>', html, flags=re.DOTALL)

    # 行内代码
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)

    # 标题
    lines = html.split('\n')
    new_lines = []
    for line in lines:
        s = line.strip()
        if s.startswith('#### '):
            new_lines.append('<h4>' + s[5:] + '</h4>')
        elif s.startswith('### '):
            new_lines.append('<h3>' + s[4:] + '</h3>')
        elif s.startswith('## '):
            new_lines.append('<h2>' + s[3:] + '</h2>')
        elif s.startswith('# '):
            new_lines.append('<h1>' + s[2:] + '</h1>')
        elif re.match(r'^---+$', s) or re.match(r'^\*\*\*+$', s):
            new_lines.append('<hr>')
        else:
            new_lines.append(line)
    html = '\n'.join(new_lines)

    # 引用块
    def process_bq(m):
        content = '<br>'.join(l.strip() for l in m.group(1).strip().split('\n') if l.strip())
        return '<blockquote><p>' + content + '</p></blockquote>'
    html = re.sub(r'^> (.+)$', process_bq, html, flags=re.MULTILINE)

    # 强调
    html = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'__([^_]+)__', r'<strong>\1</strong>', html)
    html = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', html)

    # 链接
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)

    # 列表
    html = re.sub(r'^- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'^\d+\. (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)

    # 段落处理
    paragraphs = []
    in_list = False
    in_pre = False

    for line in html.split('\n'):
        line = line.strip()
        if not line:
            if in_list:
                paragraphs.append('</ul>')
                in_list = False
            paragraphs.append('<p>&nbsp;</p>')
            continue
        if line.startswith('<pre>'):
            in_pre = True
            paragraphs.append(line)
            continue
        if in_pre:
            paragraphs.append(line)
            if '</pre>' in line:
                in_pre = False
            continue
        if line.startswith('<li>'):
            if not in_list:
                paragraphs.append('<ul>')
                in_list = True
            paragraphs.append(line)
            continue
        if line.startswith(('<h', '<hr', '<blockquote', '<img', '<table')):
            if in_list:
                paragraphs.append('</ul>')
                in_list = False
            paragraphs.append(line)
            continue
        if in_list:
            paragraphs.append('</ul>')
            in_list = False
        paragraphs.append('<p>' + line + '</p>')

    if in_list:
        paragraphs.append('</ul>')

    return '<div id="wenyan">' + '\n'.join(paragraphs) + '</div>'


def parse_markdown_for_wechat(md: str) -> str:
    """将 Markdown 转换为微信公众号内联样式 HTML（纯内联，无 <style> 标签）"""
    html = parse_markdown(md)

    # 移除所有 <style> 标签
    html = re.sub(r'<style[^>]*>[\s\S]*?</style>', '', html, flags=re.IGNORECASE)

    # 给 #wenyan 加内联样式
    html = re.sub(
        r'<div id="wenyan">',
        '<div id="wenyan" style="max-width:700px;margin:0 auto;font-family:-apple-system,BlinkMacSystemFont,\'PingFang SC\',\'Hiragino Sans GB\',\'Microsoft YaHei\',sans-serif;line-height:1.75;font-size:16px;color:#333;word-break:break-word;">',
        html
    )

    # 各标签内联样式
    styles = {
        'h1': 'text-align:center;font-size:1.6em;font-weight:bold;color:#000;margin:2em 0 1.5em;padding-bottom:0.3em;border-bottom:2px solid #000;',
        'h2': 'font-size:1.3em;font-weight:bold;color:#000;margin:1.8em 0 0.5em;',
        'h3': 'font-size:1.15em;font-weight:bold;color:#222;margin:1.5em 0 0.5em;',
        'h4': 'font-size:1.05em;font-weight:bold;color:#222;margin:0.5em 0;',
        'p': 'margin:0;padding:8px 0;letter-spacing:0.5px;line-height:1.75;',
        'strong': 'color:#000;font-weight:bold;',
        'em': 'color:#666;font-style:italic;',
        'a': 'color:#000;text-decoration:none;border-bottom:1px solid #000;',
        'ul': 'padding-left:1.5em;margin:12px 0;',
        'li': 'margin-bottom:0.5em;line-height:1.75;',
        'img': 'max-width:100%;height:auto;display:block;margin:1.5em auto;border-radius:4px;',
        'hr': 'border:none;border-top:1px solid #999;margin:2.5em 0;',
        'blockquote': 'background:#f9f9f9;border-left:4px solid #000;margin:1.5em 0;padding:1em 1em 1em 2em;color:#555;font-size:0.95em;',
        'table': 'border-collapse:collapse;margin:1.5em auto;width:100%;',
        'th': 'font-weight:bold;background:#e6e6e6;padding:10px 14px;border:1px solid #ccc;text-align:left;',
        'td': 'padding:10px 14px;border:1px solid #ccc;',
    }

    for tag, style in styles.items():
        pattern = '<' + tag + '(?![^>]*style=)([^>]*)>'
        replacement = '<' + tag + '\\1 style="' + style + '">'
        html = re.sub(pattern, replacement, html)

    html = re.sub(
        r'<code(?![^>]*style=)([^>]*)>',
        r'<code\1 style="font-family:Consolas,Monaco,monospace;font-size:0.85em;color:#000;background:#f0f0f0;padding:3px 6px;border-radius:3px;">',
        html
    )
    html = re.sub(
        r'<pre(?![^>]*style=)([^>]*)>',
        r'<pre\1 style="background:#1a1a1a;padding:1em;border-radius:6px;margin:1.5em 0;overflow-x:auto;">',
        html
    )

    return html
