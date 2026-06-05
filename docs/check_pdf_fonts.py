"""PDFのフォント情報を詳細に表示するスクリプト"""
import sys
import fitz  # PyMuPDF

def check_fonts(pdf_path: str) -> None:
    doc = fitz.open(pdf_path)
    all_fonts = {}
    type3_count = 0
    total_count = 0

    for page_num in range(len(doc)):
        page = doc[page_num]
        fonts = page.get_fonts(full=True)
        for f in fonts:
            xref, ext, ftype, name, enc, ref_name = f[0], f[1], f[2], f[3], f[4], f[5] if len(f) > 5 else ""
            key = (name, ftype, enc)
            if key not in all_fonts:
                all_fonts[key] = {"pages": [], "xref": xref}
                total_count += 1
                if "Type3" in str(ftype) or "type3" in str(ftype).lower():
                    type3_count += 1
            all_fonts[key]["pages"].append(page_num + 1)

    print(f"\n=== フォント情報: {pdf_path} ===")
    print(f"総フォント数: {total_count}")
    print(f"Type 3 フォント数: {type3_count}")
    print(f"\n{'フォント名':<40} {'タイプ':<15} {'エンコード':<15}")
    print("-" * 70)
    for (name, ftype, enc), info in sorted(all_fonts.items()):
        print(f"{name:<40} {ftype:<15} {enc:<15}")

    doc.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("使い方: python check_pdf_fonts.py <PDFファイル>")
        sys.exit(1)
    check_fonts(sys.argv[1])
