import fitz
import re
from pathlib import Path

md_path = Path("docs/Exercise_Guide.md")
pdf_path = Path("docs/Exercise_Guide_embedded.pdf")

content = md_path.read_text(encoding="utf-8")
lines = content.splitlines()

toc_start = -1
toc_end = -1
for i, line in enumerate(lines):
    if line.strip() == "## 目次":
        toc_start = i + 1
    elif toc_start != -1 and i > toc_start:
        if line.strip() == "<div style=\"page-break-before: always;\"></div>":
            toc_end = i
            break

toc_lines = lines[toc_start:toc_end]
doc = fitz.open(pdf_path)

normalized_pages = []
for i in range(len(doc)):
    text = doc[i].get_text()
    norm_text = re.sub(r'\s+', '', text)
    normalized_pages.append(norm_text)

new_toc_lines = []
for line in toc_lines:
    if "...... p." in line:
        m = re.match(r'^(\s*-\s+)(.+?)\s+...... p\.\d+$', line)
        if m:
            prefix = m.group(1)
            title = m.group(2).strip()
            
            search_title = re.sub(r'\s+', '', title)
            
            found_page = -1
            for page_idx in range(4, len(normalized_pages)):
                if search_title in normalized_pages[page_idx]:
                    found_page = page_idx + 1
                    break
            
            if found_page == -1:
                short_title = search_title[:10]
                for page_idx in range(4, len(normalized_pages)):
                    if short_title in normalized_pages[page_idx]:
                        found_page = page_idx + 1
                        break
                        
            if found_page != -1:
                new_toc_lines.append(f"{prefix}{title} ...... p.{found_page}")
            else:
                new_toc_lines.append(line)
        else:
            new_toc_lines.append(line)
    else:
        new_toc_lines.append(line)

new_content = "\n".join(lines[:toc_start] + new_toc_lines + lines[toc_end:])
md_path.write_text(new_content, encoding="utf-8")
print("TOC updated successfully by PDF parsing.")
