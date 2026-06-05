"""
Markdown → PDF 変換スクリプト (PyMuPDF Story API 直接使用)

使い方:
  python md_to_pdf.py Exercise_Guide.md
  python md_to_pdf.py Comprehensive_Design_Specification.md

出力: 同じディレクトリに [ファイル名]_embedded.pdf が生成されます。
"""

import sys
import os
import re
import fitz  # PyMuPDF
import markdown as md_lib


def build_css() -> str:
    """PDF出力用のCSSを生成する。"""
    return """
body {
    font-family: sans-serif;
    font-size: 10.5pt;
    line-height: 1.7;
    color: #333;
}
h1 {
    font-size: 1.7em;
    color: #1a365d;
    border-bottom: 2px solid #1a365d;
    padding-bottom: 5px;
    margin-top: 20px;
}
h2 {
    font-size: 1.3em;
    color: #1a365d;
    border-bottom: 1px solid #ccc;
    padding-bottom: 4px;
    margin-top: 18px;
}
h3 {
    font-size: 1.1em;
    color: #2c3e50;
    margin-top: 15px;
}
h4 {
    font-size: 1.0em;
    color: #34495e;
    margin-top: 12px;
}
pre {
    background-color: #f5f5f5;
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 8px 10px;
    font-size: 9pt;
    line-height: 1.4;
}
code {
    font-family: monospace;
    font-size: 9pt;
}
table {
    border-collapse: collapse;
    width: 100%;
    margin: 8px 0;
    font-size: 9.5pt;
}
th, td {
    border: 1px solid #ccc;
    padding: 5px 8px;
    text-align: left;
}
th {
    background-color: #f0f0f0;
    font-weight: bold;
}
img {
    max-width: 100%;
}
ul, ol {
    padding-left: 22px;
}
li {
    margin-bottom: 2px;
}
hr {
    border: none;
    border-top: 1px solid #ccc;
    margin: 12px 0;
}
blockquote {
    border-left: 4px solid #007bff;
    padding: 6px 10px;
    margin: 8px 0;
    background-color: #f8f9fa;
    font-size: 10pt;
}
"""


def preprocess_markdown(md_content: str, base_dir: str) -> str:
    """Markdownコンテンツを前処理する。"""

    # <style> ブロックを除去
    md_content = re.sub(
        r'<style>.*?</style>',
        '',
        md_content,
        flags=re.DOTALL
    )

    # page-break div を <hr> に変換（Story APIではpage-breakが使えないため）
    md_content = re.sub(
        r'<div\s+style\s*=\s*"page-break-before:\s*always;?\s*"\s*>\s*</div>',
        '\n---\n',
        md_content,
        flags=re.IGNORECASE
    )

    # HTML img タグの src 属性を絶対パスに変換
    def fix_html_img(match):
        full_tag = match.group(0)
        src = match.group(1)
        if src.startswith(('http://', 'https://', 'file://', 'data:')):
            return full_tag
        abs_path = os.path.abspath(os.path.join(base_dir, src))
        return full_tag.replace(f'src="{src}"', f'src="{abs_path}"')

    md_content = re.sub(
        r'<img\s+[^>]*?src="([^"]*)"[^>]*?>',
        fix_html_img,
        md_content,
        flags=re.IGNORECASE
    )

    # Markdown形式の画像 ![alt](path) を絶対パスに変換
    def fix_md_img(match):
        alt = match.group(1)
        src = match.group(2)
        if src.startswith(('http://', 'https://', 'file://', 'data:')):
            return match.group(0)
        abs_path = os.path.abspath(os.path.join(base_dir, src))
        return f'![{alt}]({abs_path})'

    md_content = re.sub(
        r'!\[([^\]]*)\]\(([^)]*)\)',
        fix_md_img,
        md_content
    )

    # Mermaidコードブロックを通常のコードブロックに変換
    md_content = re.sub(
        r'```mermaid',
        '```',
        md_content
    )

    return md_content


def md_to_html(md_content: str) -> str:
    """MarkdownをHTMLに変換する。"""
    extensions = [
        'tables',
        'fenced_code',
        'codehilite',
        'md_in_html',
        'sane_lists',
    ]
    extension_configs = {
        'codehilite': {
            'css_class': 'codehilite',
            'guess_lang': False,
            'noclasses': True,  # インラインスタイルを使用
        },
    }
    return md_lib.markdown(
        md_content,
        extensions=extensions,
        extension_configs=extension_configs,
    )


def convert_md_to_pdf(md_path: str) -> None:
    """MarkdownファイルをPDFに変換する。"""
    md_path = os.path.abspath(md_path)
    base_dir = os.path.dirname(md_path)
    base_name = os.path.splitext(os.path.basename(md_path))[0]
    pdf_path = os.path.join(base_dir, f"{base_name}_embedded.pdf")

    print(f"読み込み中: {md_path}")

    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Markdown前処理
    print("前処理中...")
    md_content = preprocess_markdown(md_content, base_dir)

    # Markdown → HTML
    print("HTML変換中...")
    html_body = md_to_html(md_content)

    # CSSを組み立て
    css = build_css()

    # 完全なHTML
    full_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<style>{css}</style>
</head>
<body>
{html_body}
</body>
</html>"""

    # PyMuPDF Story APIでPDF生成
    print("PDF生成中...")

    # A4用紙のサイズ
    A4 = fitz.paper_rect("A4")
    # マージン (上, 右, 下, 左) in points
    margin = 50
    where = A4 + (margin, margin, -margin, -margin)

    story = fitz.Story(html=full_html, archive=base_dir)

    writer = fitz.DocumentWriter(pdf_path)
    more = True
    while more:
        dev = writer.begin_page(A4)
        more, _ = story.place(where)
        story.draw(dev)
        writer.end_page()

    writer.close()

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
