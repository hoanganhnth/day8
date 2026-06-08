"""
Task 8 — PageIndex Vectorless RAG.

Trong môi trường có PageIndex API, module này có thể thay bằng SDK thật. Với
lab offline, `pageindex_search` dùng lexical local search và đánh dấu source là
`pageindex` để đóng vai trò vectorless fallback trong pipeline.
"""

from __future__ import annotations

from src.task6_lexical_search import lexical_search


def upload_documents() -> None:
    """Placeholder upload hook for a real PageIndex account."""
    print("Offline mode: documents are read from local data/standardized.")


def pageindex_search(query: str, top_k: int = 5) -> list[dict]:
    """
    Vectorless fallback retrieval.

    Returns:
        List of {'content': str, 'score': float, 'metadata': dict, 'source': 'pageindex'}
    """
    results = lexical_search(query, top_k=top_k)
    formatted = []
    for result in results:
        item = result.copy()
        item["source"] = "pageindex"
        formatted.append(item)
    return formatted


if __name__ == "__main__":
    for result in pageindex_search("hình phạt sử dụng ma tuý", top_k=3):
        print(f"[{result['score']:.3f}] {result['content'][:100]}...")
