"""
Task 3 — Convert sang Markdown bằng MarkItDown.

Convert toàn bộ file trong data/landing/{legal,news} sang Markdown, lưu vào
data/standardized/ giữ nguyên cấu trúc thư mục con.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANDING = ROOT / "data" / "landing"
STANDARDIZED = ROOT / "data" / "standardized"


def convert_all() -> int:
    """Convert landing -> standardized. Trả về số file đã ghi."""
    from markitdown import MarkItDown  # import trong hàm để không bắt buộc cài

    converter = MarkItDown()
    written = 0
    for category in ("legal", "news"):
        src_dir = LANDING / category
        dst_dir = STANDARDIZED / category
        dst_dir.mkdir(parents=True, exist_ok=True)
        if not src_dir.exists():
            continue
        for path in sorted(src_dir.iterdir()):
            if path.suffix.lower() == ".json":
                # Bài báo crawl về dạng JSON: lấy thẳng content_markdown.
                data = json.loads(path.read_text(encoding="utf-8"))
                text = data.get("content_markdown", "")
            else:
                text = converter.convert(str(path)).text_content
            (dst_dir / f"{path.stem}.md").write_text(text, encoding="utf-8")
            written += 1
    return written


if __name__ == "__main__":
    try:
        count = convert_all()
        print(f"Đã convert {count} file sang {STANDARDIZED}")
    except ImportError:
        print("Chưa cài markitdown. Cài: pip install markitdown")
