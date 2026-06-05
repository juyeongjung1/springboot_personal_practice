"""
Markdown → PDF 変換スクリプト (Playwright & Chromium 使用)

使い方:
  python md_to_pdf.py Exercise_Guide.md
  python md_to_pdf.py Comprehensive_Design_Specification.md

出力: 同じディレクトリに [ファイル名]_embedded.pdf が生成されます。
"""

import sys
import os
import re
import html
import markdown as md_lib
from playwright.sync_api import sync_playwright

def process_github_alerts(md_text: str) -> str:
    """GitHubスタイルの警告ブロック（> [!NOTE]など）をHTMLのdivブロックに変換する。"""
    lines = md_text.split('\n')
    new_lines = []
    in_quote = False
    alert_type = None
    alert_content = []
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('>'):
            content = stripped.lstrip('>').strip()
            # アラートのヘッダー [!NOTE] などを検出
            m = re.match(r'^\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]$', content, re.IGNORECASE)
            if m:
                alert_type = m.group(1).upper()
                in_quote = True
                continue
            
            if in_quote and alert_type:
                alert_content.append(content)
            else:
                new_lines.append(line)
        else:
            if in_quote and alert_type:
                # 引用ブロック終了。アラートのdivを構築する
                alert_body = '\n'.join(alert_content)
                # markdown="1" を指定して内部のMarkdownもパースさせる
                box_html = f'<div class="markdown-alert markdown-alert-{alert_type.lower()}" markdown="1">\n'
                title_map = {
                    'NOTE': '補足',
                    'TIP': 'ヒント',
                    'IMPORTANT': '重要',
                    'WARNING': '注意',
                    'CAUTION': '警告',
                }
                box_html += f'<p class="markdown-alert-title">{title_map.get(alert_type, alert_type)}</p>\n'
                box_html += alert_body + "\n</div>\n"
                new_lines.append(box_html)
                in_quote = False
                alert_type = None
                alert_content = []
            new_lines.append(line)
            
    if in_quote and alert_type:
        alert_body = '\n'.join(alert_content)
        box_html = f'<div class="markdown-alert markdown-alert-{alert_type.lower()}" markdown="1">\n'
        title_map = {
            'NOTE': '補足',
            'TIP': 'ヒント',
            'IMPORTANT': '重要',
            'WARNING': '注意',
            'CAUTION': '警告',
        }
        box_html += f'<p class="markdown-alert-title">{title_map.get(alert_type, alert_type)}</p>\n'
        box_html += alert_body + "\n</div>\n"
        new_lines.append(box_html)
        
    return '\n'.join(new_lines)

def normalize_tables(md_text: str) -> str:
    lines = md_text.split('\n')
    new_lines = []
    in_table = False

    def is_table_line(line: str) -> bool:
        stripped = line.strip()
        return stripped.startswith('|') and stripped.endswith('|') and stripped.count('|') >= 2

    for line in lines:
        table_line = is_table_line(line)

        if table_line and not in_table and new_lines and new_lines[-1].strip():
            new_lines.append('')

        if not table_line and in_table and line.strip():
            new_lines.append('')

        new_lines.append(line)
        in_table = table_line

    return '\n'.join(new_lines)

def normalize_nested_lists(md_text: str) -> str:
    lines = md_text.split('\n')
    new_lines = []
    in_nested_list = False

    def is_nested_list(line: str) -> bool:
        return bool(re.match(r'^\s{2,}-\s+', line))

    for line in lines:
        nested_list = is_nested_list(line)

        if nested_list and not in_nested_list and new_lines and new_lines[-1].strip():
            new_lines.append('')

        if not nested_list and in_nested_list and line.strip():
            new_lines.append('')

        new_lines.append(line)
        in_nested_list = nested_list

    return '\n'.join(new_lines)

def remove_css_page_footer(css: str) -> str:
    return re.sub(r'@bottom-center\s*\{[^{}]*\}', '', css, flags=re.DOTALL)

def render_toc_section(md_text: str) -> str:
    def replace_toc(match):
        toc_lines = match.group(1).splitlines()
        items = []
        for line in toc_lines:
            stripped = line.strip()
            if not stripped.startswith('- '):
                continue

            level = 2 if line.startswith('  ') else 1
            content = stripped[2:].strip()
            page = ''
            title = content
            page_match = re.match(r'(.+?)\s*\.{3,}\s*(p\.\d+)\s*$', content)
            if page_match:
                title = page_match.group(1).strip()
                page = page_match.group(2).strip()

            page_html = f'<span class="toc-page">{html.escape(page)}</span>' if page else ''
            items.append(
                f'<li class="toc-item toc-level-{level}">'
                f'<span class="toc-title">{html.escape(title)}</span>'
                f'{page_html}</li>'
            )

        toc_html = '\n'.join(items)
        return f'## 目次\n\n<section class="toc-section">\n<ul class="toc-list">\n{toc_html}\n</ul>\n</section>\n'

    return re.sub(
        r'## 目次\s*\n(.*?)(?=\n<div style="page-break-before: always;"></div>)',
        replace_toc,
        md_text,
        count=1,
        flags=re.DOTALL
    )

def build_default_css() -> str:
    """PDF出力用の基本CSSスタイル。"""
    return """
    body {
        font-family: "BIZ UDGothic", "Meiryo", "MS Gothic", "Hiragino Kaku Gothic ProN", sans-serif;
        font-size: 10.8pt;
        line-height: 1.82;
        color: #263238;
        margin: 0;
        padding: 0;
    }
    p {
        margin: 0 0 12px;
    }
    h1 {
        font-size: 1.85em;
        color: #123a5f;
        border-bottom: 2px solid #123a5f;
        padding-bottom: 7px;
        margin-top: 28px;
        margin-bottom: 18px;
        page-break-after: avoid;
    }
    h2 {
        font-size: 1.42em;
        color: #123a5f;
        border-bottom: 1px solid #cfd8dc;
        padding-bottom: 6px;
        margin-top: 24px;
        margin-bottom: 14px;
        page-break-after: avoid;
    }
    h3 {
        font-size: 1.14em;
        color: #1f4e79;
        margin-top: 20px;
        margin-bottom: 10px;
        page-break-after: avoid;
    }
    ul, ol {
        margin-top: 8px;
        margin-bottom: 14px;
        padding-left: 1.7em;
    }
    li {
        margin-bottom: 7px;
        line-height: 1.75;
    }
    li > ul, li > ol {
        margin-top: 6px;
        margin-bottom: 8px;
    }
    strong {
        color: #123a5f;
        font-weight: 700;
    }
    em {
        color: #52616b;
        font-style: normal;
    }
    a {
        color: #0b65c2;
        text-decoration: none;
        font-weight: 600;
    }
    hr {
        border: none;
        border-top: 2px solid #d6dde3;
        margin: 22px 0;
    }
    pre {
        background-color: #f4f7fb;
        border: 1px solid #c8d5e3;
        border-left: 5px solid #2f6f9f;
        border-radius: 6px;
        padding: 12px 14px;
        margin: 12px 0 18px;
        font-size: 9.2pt;
        line-height: 1.55;
        white-space: pre-wrap;
        overflow-wrap: anywhere;
        page-break-inside: avoid;
    }
    code {
        font-family: "Consolas", Courier, monospace;
        font-size: 0.9em;
        background-color: #eef3f8;
        border: 1px solid #d4dee8;
        border-radius: 4px;
        color: #263f5e;
        padding: 1px 4px;
    }
    pre code {
        background: transparent;
        border: none;
        color: #263238;
        padding: 0;
        font-size: inherit;
    }
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 16px 0 20px;
        font-size: 9.6pt;
        page-break-inside: avoid;
    }
    th, td {
        border: 1px solid #cdd6df;
        padding: 7px 10px;
        text-align: left;
    }
    th {
        background-color: #edf3f8;
        color: #123a5f;
        font-weight: bold;
    }
    img {
        max-width: 100%;
        height: auto;
        display: block;
        margin: 10px auto;
    }
    
    /* GitHub アラートのスタイル */
    .markdown-alert {
        padding: 13px 16px;
        margin: 16px 0 20px;
        border-left: 5px solid;
        border-radius: 6px;
        page-break-inside: avoid;
    }
    .markdown-alert-note {
        border-left-color: #007bff;
        background-color: #e9f5ff;
    }
    .markdown-alert-note .markdown-alert-title {
        color: #007bff;
    }
    .markdown-alert-tip {
        border-left-color: #28a745;
        background-color: #f0fcf4;
    }
    .markdown-alert-tip .markdown-alert-title {
        color: #28a745;
    }
    .markdown-alert-important {
        border-left-color: #8957e5;
        background-color: #f8f0ff;
    }
    .markdown-alert-important .markdown-alert-title {
        color: #8957e5;
    }
    .markdown-alert-warning {
        border-left-color: #ffc107;
        background-color: #fff8e1;
    }
    .markdown-alert-warning .markdown-alert-title {
        color: #ffc107;
    }
    .markdown-alert-caution {
        border-left-color: #dc3545;
        background-color: #fde8eb;
    }
    .markdown-alert-caution .markdown-alert-title {
        color: #dc3545;
    }
    .markdown-alert-title {
        font-weight: bold;
        margin-top: 0;
        margin-bottom: 7px;
        font-size: 0.98em;
    }
    .hint-box,
    .point-box {
        padding: 13px 16px;
        margin: 16px 0 20px;
        border-left: 5px solid;
        border-radius: 6px;
        page-break-inside: avoid;
    }
    .hint-box {
        background-color: #fff8e1;
        border-left-color: #ffc107;
    }
    .point-box {
        background-color: #f0fcf4;
        border-left-color: #28a745;
    }
    .hint-box strong,
    .point-box strong {
        display: block;
        margin-bottom: 6px;
    }
    .hint-box strong {
        color: #856404;
    }
    .point-box strong {
        color: #1f7a3a;
    }
    .screen-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 14px;
        margin: 16px 0 22px;
    }
    .screen-grid-single {
        grid-template-columns: minmax(0, 1fr);
    }
    .screen-card {
        margin: 0;
        padding: 11px;
        background-color: #f7fafc;
        border: 1px solid #cdd6df;
        border-radius: 6px;
        page-break-inside: avoid;
    }
    .screen-card figcaption {
        color: #123a5f;
        font-weight: 700;
        font-size: 0.94em;
        line-height: 1.45;
        margin-bottom: 8px;
    }
    .screen-card img {
        width: 100%;
        max-height: 270px;
        object-fit: contain;
        margin: 0 auto;
        border: 1px solid #e0e6ec;
        border-radius: 4px;
        background-color: #ffffff;
    }
    .flow-diagram {
        padding: 16px;
        margin: 14px 0 22px;
        background-color: #f4f7fb;
        border: 1px solid #c8d5e3;
        border-left: 5px solid #2f6f9f;
        border-radius: 6px;
        page-break-inside: avoid;
    }
    .flow-row {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        margin: 9px 0;
        flex-wrap: wrap;
    }
    .flow-node {
        min-width: 110px;
        padding: 8px 12px;
        background-color: #ffffff;
        border: 1px solid #b8cad9;
        border-radius: 5px;
        color: #123a5f;
        font-weight: 700;
        text-align: center;
        line-height: 1.35;
    }
    .flow-note {
        color: #52616b;
        font-size: 0.9em;
        font-weight: 600;
    }
    .flow-arrow {
        color: #2f6f9f;
        font-weight: 700;
    }
    .er-diagram {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 12px;
        margin: 14px 0 22px;
        page-break-inside: avoid;
    }
    .er-card {
        border: 1px solid #c8d5e3;
        border-radius: 6px;
        background-color: #f7fafc;
        overflow: hidden;
    }
    .er-card h3 {
        margin: 0;
        padding: 8px 10px;
        background-color: #1f4e79;
        color: #ffffff;
        font-size: 1em;
    }
    .er-card ul {
        margin: 0;
        padding: 10px 12px 12px 24px;
    }
    .er-rel {
        grid-column: 1 / -1;
        padding: 10px 12px;
        background-color: #e9f5ff;
        border-left: 5px solid #007bff;
        border-radius: 6px;
        color: #123a5f;
        font-weight: 700;
        text-align: center;
    }
    .toc-section {
        padding: 2px 0 0;
    }
    .toc-list {
        list-style: none;
        padding-left: 0;
        margin: 0;
    }
    .toc-item {
        display: flex;
        justify-content: space-between;
        gap: 12px;
        margin: 8px 0;
        padding: 7px 10px;
        border-left: 4px solid #1f6aa5;
        background-color: #f6f9fc;
        color: #123a5f;
        font-weight: 700;
        line-height: 1.45;
        page-break-inside: avoid;
    }
    .toc-level-2 {
        margin-left: 26px;
        padding-top: 5px;
        padding-bottom: 5px;
        border-left: 2px solid #c5d3df;
        background-color: #ffffff;
        color: #3d4f5c;
        font-weight: 500;
        font-size: 0.93em;
    }
    .toc-title {
        flex: 1;
    }
    .toc-page {
        flex: 0 0 auto;
        color: #1f4e79;
        font-weight: 700;
    }
    
    /* カスタムボックス */
    div[style*="background-color: #e9f5ff"] {
        background-color: #e9f5ff !important;
        border-left: 5px solid #007bff !important;
        padding: 14px 16px !important;
        margin: 16px 0 20px !important;
        border-radius: 6px !important;
        page-break-inside: avoid;
    }
    div[style*="background-color: #fff3cd"] {
        background-color: #fff3cd !important;
        border-left: 5px solid #ffecb5 !important;
        padding: 12px 14px !important;
        margin-top: 12px !important;
        margin-bottom: 14px !important;
        border-radius: 6px !important;
        page-break-inside: avoid;
    }
    """

def convert_md_to_pdf(md_path: str) -> None:
    """MarkdownファイルをPDFに変換する。"""
    md_path = os.path.abspath(md_path)
    base_dir = os.path.dirname(md_path)
    base_name = os.path.splitext(os.path.basename(md_path))[0]
    pdf_path = os.path.join(base_dir, f"{base_name}_embedded.pdf")

    print(f"読み込み中: {md_path}")
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Markdown埋め込みのスタイルシートを抽出
    embedded_styles = ""
    style_match = re.search(r'<style>(.*?)</style>', md_content, flags=re.DOTALL)
    if style_match:
        embedded_styles = remove_css_page_footer(style_match.group(1))

    # Markdownコンテンツから <style> タグを除去する
    md_content = re.sub(r'<style>.*?</style>', '', md_content, flags=re.DOTALL)
    md_content = render_toc_section(md_content)

    # GitHubアラートを置換
    md_content = process_github_alerts(md_content)
    md_content = normalize_tables(md_content)
    md_content = normalize_nested_lists(md_content)

    # Mermaidコードブロックを <pre class="mermaid"> に置換
    def replace_mermaid(match):
        code = match.group(1).strip()
        code_esc = html.escape(code)
        return f'<pre class="mermaid">{code_esc}</pre>'
    md_content = re.sub(r'```mermaid\n(.*?)\n```', replace_mermaid, md_content, flags=re.DOTALL)

    # Markdown → HTML 変換
    print("HTML変換中...")
    extensions = ['tables', 'fenced_code', 'codehilite', 'md_in_html', 'sane_lists']
    extension_configs = {
        'codehilite': {
            'css_class': 'codehilite',
            'guess_lang': False,
            'noclasses': True,
        },
    }
    html_body = md_lib.markdown(
        md_content,
        extensions=extensions,
        extension_configs=extension_configs
    )

    # 改ページdivのクラス置換
    html_body = html_body.replace(
        '<div style="page-break-before: always;"></div>',
        '<div class="page-break"></div>'
    )
    html_body = re.sub(r'<hr\s*/?>\s*<div class="page-break"></div>', '<div class="page-break"></div>', html_body)

    # 基本CSS
    default_css = build_default_css()

    # 追加のプリントスタイル
    print_styles = """
    @media print {
        * {
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }
        @page {
            margin-top: 20mm;
            margin-bottom: 20mm;
        }
        div.page-break {
            page-break-before: always;
            height: 0;
            margin: 0;
            border: none;
        }
    }
    """

    # 完全なHTML文書を作成
    full_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<style>
{default_css}
{embedded_styles}
{print_styles}
</style>
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
  mermaid.initialize({{
    startOnLoad: true,
    theme: 'default',
    securityLevel: 'loose'
  }});
</script>
</head>
<body>
{html_body}
</body>
</html>"""

    # 一時的なHTMLファイルを同一ディレクトリに保存（相対画像の解決のため）
    temp_html_path = os.path.join(base_dir, f"_temp_{base_name}.html")
    with open(temp_html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

    print("Playwright で PDF を生成中...")
    with sync_playwright() as p:
        # '--font-render-hinting=none' を指定してType 3フォントの発生を防ぐ
        browser = p.chromium.launch(args=['--font-render-hinting=none'])
        page = browser.new_page()

        # file:// プロトコルで一時HTMLを読み込む
        abs_html_path = os.path.abspath(temp_html_path).replace('\\', '/')
        page.goto(f"file:///{abs_html_path}")

        # フォントが完全にロードされるのを待つ
        page.evaluate("document.fonts.ready")

        # ページ上にMermaidの要素がある場合、レンダリング完了を待つ
        if "<pre class=\"mermaid\">" in html_body:
            print("Mermaid レンダリング完了を待機中...")
            try:
                page.wait_for_selector('.mermaid[data-processed="true"]', timeout=10000)
                print("Mermaid レンダリング完了")
            except Exception as e:
                print(f"警告: Mermaid レンダリングの待機中にタイムアウトしました。: {e}")
                page.wait_for_timeout(3000)

        # PDF印刷用のフッターテンプレート (ページ番号の中央下部配置)
        footer_template = (
            '<div style="font-size: 9pt; width: 100%; text-align: center; '
            'color: #666; font-family: \'BIZ UDGothic\', \'Meiryo\', sans-serif;">'
            '- <span class="pageNumber"></span> -</div>'
        )

        page.pdf(
            path=pdf_path,
            format="A4",
            margin={"top": "20mm", "right": "15mm", "bottom": "20mm", "left": "15mm"},
            print_background=True,
            display_header_footer=True,
            header_template="<span></span>",  # ヘッダーは非表示
            footer_template=footer_template
        )
        browser.close()

    # 一時ファイルのクリーンアップ
    if os.path.exists(temp_html_path):
        os.remove(temp_html_path)

    print(f"完了: {pdf_path}")
    print(f"ファイルサイズ: {os.path.getsize(pdf_path) / 1024:.1f} KB")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("使い方: python md_to_pdf.py <markdownファイル>")
        print("例: python md_to_pdf.py Exercise_Guide.md")
        sys.exit(1)

    for md_file in sys.argv[1:]:
        if not os.path.exists(md_file):
            print(f"エラー: ファイルが見つかりません: {md_file}")
            continue
        convert_md_to_pdf(md_file)
