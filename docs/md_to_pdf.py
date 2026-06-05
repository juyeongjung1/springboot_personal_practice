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
                box_html += f'<p class="markdown-alert-title">{alert_type}</p>\n'
                box_html += alert_body + "\n</div>\n"
                new_lines.append(box_html)
                in_quote = False
                alert_type = None
                alert_content = []
            new_lines.append(line)
            
    if in_quote and alert_type:
        alert_body = '\n'.join(alert_content)
        box_html = f'<div class="markdown-alert markdown-alert-{alert_type.lower()}" markdown="1">\n'
        box_html += f'<p class="markdown-alert-title">{alert_type}</p>\n'
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

def remove_css_page_footer(css: str) -> str:
    return re.sub(r'@bottom-center\s*\{[^{}]*\}', '', css, flags=re.DOTALL)

def apply_page_break_hints(md_text: str) -> str:
    marker = '   - `<form>` 要素に `th:object="${bookForm}"` を設定し、各入力欄'
    replacement = '<div style="page-break-before: always;"></div>\n\n' + marker
    return md_text.replace(marker, replacement, 1)

def build_default_css() -> str:
    """PDF出力用の基本CSSスタイル。"""
    return """
    body {
        font-family: "BIZ UDGothic", "Meiryo", "MS Gothic", "Hiragino Kaku Gothic ProN", sans-serif;
        font-size: 11pt;
        line-height: 1.8;
        color: #333;
        margin: 0;
        padding: 0;
    }
    h1 {
        font-size: 1.8em;
        color: #1a365d;
        border-bottom: 2px solid #1a365d;
        padding-bottom: 5px;
        margin-top: 25px;
        margin-bottom: 15px;
        page-break-after: avoid;
    }
    h2 {
        font-size: 1.4em;
        color: #1a365d;
        border-bottom: 1px solid #ccc;
        padding-bottom: 4px;
        margin-top: 20px;
        margin-bottom: 12px;
        page-break-after: avoid;
    }
    h3 {
        font-size: 1.1em;
        color: #2c3e50;
        margin-top: 15px;
        margin-bottom: 8px;
        page-break-after: avoid;
    }
    pre {
        background-color: #f5f5f5;
        border: 1px solid #ddd;
        border-radius: 4px;
        padding: 8px 10px;
        font-size: 9pt;
        line-height: 1.4;
        overflow: auto;
    }
    code {
        font-family: "Consolas", Courier, monospace;
        font-size: 9pt;
    }
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 15px 0;
        font-size: 9.5pt;
    }
    th, td {
        border: 1px solid #ccc;
        padding: 6px 10px;
        text-align: left;
    }
    th {
        background-color: #f0f0f0;
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
        padding: 10px 15px;
        margin-bottom: 15px;
        border-left: 0.25em solid;
        border-radius: 4px;
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
        margin-bottom: 5px;
        font-size: 0.95em;
    }
    
    /* カスタムボックス */
    div[style*="background-color: #e9f5ff"] {
        background-color: #e9f5ff !important;
        border-left: 5px solid #007bff !important;
        padding: 15px !important;
        margin-bottom: 20px !important;
        border-radius: 5px !important;
    }
    div[style*="background-color: #fff3cd"] {
        background-color: #fff3cd !important;
        border-left: 5px solid #ffecb5 !important;
        padding: 10px !important;
        margin-top: 10px !important;
        margin-bottom: 10px !important;
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

    # GitHubアラートを置換
    md_content = process_github_alerts(md_content)
    md_content = normalize_tables(md_content)
    md_content = apply_page_break_hints(md_content)

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
