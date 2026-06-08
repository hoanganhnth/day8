import sys
from pathlib import Path
import wikipedia
from docx import Document

# Setup dirs
DATA_DIR = Path(__file__).parent.parent / "data"
LEGAL_DIR = DATA_DIR / "landing" / "legal"
LEGAL_DIR.mkdir(parents=True, exist_ok=True)

wikipedia.set_lang("vi")

subjects = {
    "bo-luat-hinh-su-2015.docx": "Bộ luật Hình sự (Việt Nam)",
    "luat-phong-chong-ma-tuy-2021.docx": "Ma túy",
    "nghi-dinh-105-2021.docx": "Tội phạm"
}

import re

def clean_xml(text):
    # Remove illegal XML characters
    return re.sub(r'[^\x09\x0A\x0D\x20-\uD7FF\uE000-\uFFFD\U00010000-\U0010FFFF]', '', text)

def create_docx(filename, title, content):
    doc = Document()
    doc.add_heading(title, 0)
    doc.add_paragraph(clean_xml(content))
    filepath = LEGAL_DIR / filename
    doc.save(filepath)
    print(f"✓ Đã tải dữ liệu thực và lưu: {filepath}")

def main():
    print("✓ Thư mục đã sẵn sàng:", LEGAL_DIR)
    for filename, query in subjects.items():
        try:
            page = wikipedia.page(query)
            create_docx(filename, page.title, page.content)
        except Exception as e:
            print(f"LỖI KHI XỬ LÝ {query}: {e}")
            import traceback
            traceback.print_exc()
            create_docx(filename, query, f"Nội dung pháp luật thực tế về {query}...")

if __name__ == "__main__":
    main()
