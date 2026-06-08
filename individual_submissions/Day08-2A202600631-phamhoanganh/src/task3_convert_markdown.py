"""
Task 3 — Convert toàn bộ file trong data/landing/ thành Markdown.

Sử dụng MarkItDown của Microsoft:
    https://github.com/microsoft/markitdown

Cài đặt:
    pip install markitdown

Hướng dẫn:
    1. Scan toàn bộ file trong data/landing/ (PDF, DOCX, JSON)
    2. Convert sang Markdown
    3. Lưu vào data/standardized/ giữ nguyên cấu trúc thư mục
"""

import json
from pathlib import Path

from markitdown import MarkItDown

LANDING_DIR = Path(__file__).parent.parent / "data" / "landing"
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "standardized"


def convert_legal_docs():
    """Convert PDF/DOCX files trong data/landing/legal/ sang markdown."""
    legal_dir = LANDING_DIR / "legal"
    output_dir = OUTPUT_DIR / "legal"
    output_dir.mkdir(parents=True, exist_ok=True)

    if not legal_dir.exists():
        print("  ⚠ Thư mục data/landing/legal/ chưa tồn tại")
        return

    md = MarkItDown()
    converted = 0

    for filepath in sorted(legal_dir.iterdir()):
        if filepath.suffix.lower() in (".pdf", ".docx", ".doc"):
            print(f"  Converting: {filepath.name}")
            try:
                result = md.convert(str(filepath))
                output_path = output_dir / f"{filepath.stem}.md"
                output_path.write_text(result.text_content, encoding="utf-8")
                print(f"    ✓ Saved: {output_path.name} ({len(result.text_content):,} chars)")
                converted += 1
            except Exception as e:
                print(f"    ✗ Lỗi convert {filepath.name}: {e}")

    print(f"  → Đã convert {converted} file legal docs")


def convert_news_articles():
    """Convert JSON crawled articles trong data/landing/news/ sang markdown."""
    news_dir = LANDING_DIR / "news"
    output_dir = OUTPUT_DIR / "news"
    output_dir.mkdir(parents=True, exist_ok=True)

    if not news_dir.exists():
        print("  ⚠ Thư mục data/landing/news/ chưa tồn tại")
        return

    converted = 0

    for filepath in sorted(news_dir.iterdir()):
        if filepath.suffix.lower() == ".json":
            print(f"  Converting: {filepath.name}")
            try:
                data = json.loads(filepath.read_text(encoding="utf-8"))
                output_path = output_dir / f"{filepath.stem}.md"

                # Thêm metadata header
                header = f"# {data.get('title', 'Unknown')}\n\n"
                header += f"**Source:** {data.get('url', 'N/A')}\n"
                header += f"**Crawled:** {data.get('date_crawled', 'N/A')}\n\n---\n\n"

                content = header + data.get("content_markdown", "")
                output_path.write_text(content, encoding="utf-8")
                print(f"    ✓ Saved: {output_path.name} ({len(content):,} chars)")
                converted += 1
            except Exception as e:
                print(f"    ✗ Lỗi convert {filepath.name}: {e}")

        elif filepath.suffix.lower() in (".html", ".md", ".txt"):
            # Copy trực tiếp nếu là HTML/MD/TXT
            print(f"  Copying: {filepath.name}")
            try:
                content = filepath.read_text(encoding="utf-8")
                output_path = output_dir / f"{filepath.stem}.md"
                output_path.write_text(content, encoding="utf-8")
                print(f"    ✓ Saved: {output_path.name}")
                converted += 1
            except Exception as e:
                print(f"    ✗ Lỗi: {e}")

    print(f"  → Đã convert {converted} bài báo")


def convert_all():
    """Convert toàn bộ files."""
    print("=" * 50)
    print("Task 3: Convert to Markdown (MarkItDown)")
    print("=" * 50)

    print("\n--- Legal Documents ---")
    convert_legal_docs()

    print("\n--- News Articles ---")
    convert_news_articles()

    # Summary
    print(f"\n✓ Done! Output tại: {OUTPUT_DIR}")
    legal_files = list((OUTPUT_DIR / "legal").rglob("*.md")) if (OUTPUT_DIR / "legal").exists() else []
    news_files = list((OUTPUT_DIR / "news").rglob("*.md")) if (OUTPUT_DIR / "news").exists() else []
    print(f"  Legal: {len(legal_files)} files")
    print(f"  News: {len(news_files)} files")


if __name__ == "__main__":
    convert_all()
