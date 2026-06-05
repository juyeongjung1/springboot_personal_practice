import re
from pathlib import Path

md_path = Path("docs/Exercise_Guide.md")
content = md_path.read_text(encoding="utf-8")
lines = content.splitlines()

page_counter = 1
heading_pages = {}

# パス1: ページ数のマッピング
for line in lines:
    if line.strip() == '<div style="page-break-before: always;"></div>':
        page_counter += 1
    
    m = re.match(r'^(##|###)\s+(.+)$', line)
    if m:
        title = m.group(2).strip()
        if title not in heading_pages:
            heading_pages[title] = page_counter

# パス2: 目次の特定と置換
toc_start = -1
toc_end = -1
for i, line in enumerate(lines):
    if line.strip() == "## 目次":
        toc_start = i + 1
    elif toc_start != -1 and i > toc_start:
        if line.strip() == '<div style="page-break-before: always;"></div>':
            toc_end = i
            break

new_toc_lines = []
for line in lines[toc_start:toc_end]:
    m = re.match(r'^(\s*-\s+)(.+?)\s+...... p\.\d+$', line)
    if m:
        prefix = m.group(1)
        title = m.group(2).strip()
        
        found_page = -1
        if title in heading_pages:
            found_page = heading_pages[title]
        else:
            # "1. プロジェクトのインポート" などの完全一致を試す
            for h_title, p_num in heading_pages.items():
                if title.replace("【発展】", "").replace("【オプション】", "").strip() in h_title:
                    found_page = p_num
                    break
        
        if found_page != -1:
            new_toc_lines.append(f"{prefix}{title} ...... p.{found_page}")
        else:
            new_toc_lines.append(line)
    else:
        new_toc_lines.append(line)

new_content = "\n".join(lines[:toc_start] + new_toc_lines + lines[toc_end:])
md_path.write_text(new_content, encoding="utf-8")
print("TOC logical calculation completed.")
