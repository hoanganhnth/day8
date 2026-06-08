"""
Task 2 — Crawl bài báo.

Danh sách URL bài báo thật về nghệ sĩ Việt liên quan ma túy. Hàm crawl dùng
Crawl4AI nếu đã cài; nếu chưa, in hướng dẫn. Mỗi bài lưu thành 1 JSON trong
data/landing/news/ kèm metadata (url, title, source, date_published, date_crawled,
content_markdown).
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

LANDING_NEWS = Path(__file__).resolve().parent.parent / "data" / "landing" / "news"

NEWS_URLS = [
    "https://tuoitre.vn/xet-xu-ca-si-chau-viet-cuong-vu-giet-nu-sinh-trong-con-ngao-da-20190307070436744.htm",
    "https://tuoitre.vn/dien-vien-huu-tin-lanh-7-nam-6-thang-tu-20230428114919793.htm",
    "https://tuoitre.vn/bat-nguoi-mau-an-tay-ca-si-chi-dan-co-tien-truc-phuong-do-lien-quan-ma-tuy-20241114114826655.htm",
    "https://tuoitre.vn/nha-thiet-ke-nguyen-cong-tri-bi-bat-vi-lien-quan-ma-tuy-20250723135411525.htm",
    "https://vietnamnet.vn/ngoai-nguyen-cong-tri-nhung-nghe-si-nao-tung-bi-bat-vi-ma-tuy-2424971.html",
    "https://tuoitre.vn/chuyen-an-vn10-truy-to-227-bi-can-trong-do-co-ca-si-chi-dan-an-tay-2026040308051239.htm",
]


async def crawl_one(url: str) -> dict:
    """Crawl một URL bằng Crawl4AI (async)."""
    from crawl4ai import AsyncWebCrawler  # import trong hàm để không bắt buộc cài

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)
        return {
            "url": url,
            "title": (result.metadata or {}).get("title", ""),
            "date_crawled": datetime.now().isoformat(),
            "content_markdown": result.markdown,
        }


async def crawl_all() -> None:
    LANDING_NEWS.mkdir(parents=True, exist_ok=True)
    for index, url in enumerate(NEWS_URLS, start=1):
        article = await crawl_one(url)
        out = LANDING_NEWS / f"article_{index:02d}.json"
        out.write_text(json.dumps(article, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  saved {out.name} <- {url}")


if __name__ == "__main__":
    try:
        import asyncio

        asyncio.run(crawl_all())
    except ImportError:
        print("Chưa cài crawl4ai. Cài: pip install crawl4ai")
        print("Danh sách URL cần crawl:")
        for u in NEWS_URLS:
            print("  -", u)
