"""
Task 1 — Thu thập văn bản pháp luật.

Liệt kê các văn bản nguồn (kèm link chính thức) và kiểm tra file gốc đã có trong
data/landing/legal/ chưa. Tải file PDF/DOCX về thủ công từ cổng chính thức rồi
đặt vào thư mục này (tên file theo LEGAL_SOURCES).
"""

from __future__ import annotations

from pathlib import Path

LANDING_LEGAL = Path(__file__).resolve().parent.parent / "data" / "landing" / "legal"

LEGAL_SOURCES = [
    {
        "filename": "luat-phong-chong-ma-tuy-2021.pdf",
        "title": "Luật Phòng, chống ma túy 2021 (73/2021/QH14)",
        "url": "https://thuvienphapluat.vn/van-ban/Trach-nhiem-hinh-su/Luat-Phong-chong-ma-tuy-2021-445185.aspx",
    },
    {
        "filename": "nghi-dinh-105-2021-huong-dan-luat-phong-chong-ma-tuy.pdf",
        "title": "Nghị định 105/2021/NĐ-CP",
        "url": "https://thuvienphapluat.vn/van-ban/Van-hoa-Xa-hoi/Nghi-dinh-105-2021-ND-CP-huong-dan-Luat-Phong-chong-ma-tuy-496664.aspx",
    },
    {
        "filename": "nghi-dinh-57-2022-danh-muc-chat-ma-tuy.pdf",
        "title": "Nghị định 57/2022/NĐ-CP - danh mục chất ma túy và tiền chất",
        "url": "https://thuvienphapluat.vn/van-ban/Van-hoa-Xa-hoi/Nghi-dinh-57-2022-ND-CP-danh-muc-chat-ma-tuy-va-tien-chat-527507.aspx",
    },
    {
        "filename": "bo-luat-hinh-su-2015-chuong-xx-ma-tuy.pdf",
        "title": "Bộ luật Hình sự 2015 (100/2015/QH13) - Chương XX",
        "url": "https://thuvienphapluat.vn/van-ban/Trach-nhiem-hinh-su/Bo-luat-hinh-su-2015-296661.aspx",
    },
]


def verify_landing() -> list[dict]:
    """Kiểm tra từng nguồn đã có file trong data/landing/legal/ chưa."""
    report = []
    for source in LEGAL_SOURCES:
        path = LANDING_LEGAL / source["filename"]
        report.append({**source, "exists": path.exists(),
                       "size": path.stat().st_size if path.exists() else 0})
    return report


if __name__ == "__main__":
    LANDING_LEGAL.mkdir(parents=True, exist_ok=True)
    print(f"Kiểm tra {len(LEGAL_SOURCES)} văn bản trong {LANDING_LEGAL}:\n")
    for row in verify_landing():
        mark = "OK" if row["exists"] else "THIẾU"
        print(f"  [{mark}] {row['filename']} — {row['title']}")
        if not row["exists"]:
            print(f"         Tải tại: {row['url']}")
