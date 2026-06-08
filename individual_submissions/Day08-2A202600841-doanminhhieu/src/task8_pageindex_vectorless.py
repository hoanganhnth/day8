"""
Task 8 — PageIndex Vectorless RAG (fallback).

PageIndex (https://pageindex.ai) cho phép truy hồi không cần vector store, dựa
trên cây cấu trúc tài liệu. Khi có tài khoản + SDK, bạn upload tài liệu rồi gọi
API truy vấn. Ở chế độ offline của lab, `pageindex_search` đóng vai vectorless
bằng cách tra cứu từ khoá trên chính kho chunk và đánh dấu `source='pageindex'`,
để tầng pipeline (task9) dùng làm nhánh dự phòng khi hybrid không đủ tốt.
"""

from __future__ import annotations

import os

from src.task6_lexical_search import lexical_search

PAGEINDEX_API_KEY = os.getenv("PAGEINDEX_API_KEY", "")


def upload_to_pageindex(documents) -> dict:  # pragma: no cover - cửa cắm SDK thật
    """Hook upload khi dùng PageIndex thật. Offline: chỉ báo trạng thái."""
    if not PAGEINDEX_API_KEY:
        return {"status": "offline", "detail": "Chưa cấu hình PAGEINDEX_API_KEY."}
    raise NotImplementedError("Cắm PageIndex SDK thật tại đây khi có API key.")


def pageindex_search(query: str, top_k: int = 5) -> list[dict]:
    """
    Vectorless retrieval (fallback).

    Returns:
        list[dict] mỗi phần tử có thêm khoá 'source' = 'pageindex'.
    """
    results = lexical_search(query, top_k=top_k)
    for result in results:
        result["source"] = "pageindex"
    return results


if __name__ == "__main__":
    for hit in pageindex_search("danh mục chất ma tuý", top_k=3):
        print(f"[{hit['score']:.4f}] ({hit['source']}) {hit['content'][:70]}...")
