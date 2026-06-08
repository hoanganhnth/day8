"""
Task 5 — Semantic Search Module.

Offline fallback implementation: token-vector cosine similarity over the chunks
created in Task 4. It returns the same public shape expected from dense
retrieval: content, score, metadata sorted descending.
"""

from __future__ import annotations

from src.retrieval_utils import score_chunks
from src.task4_chunking_indexing import chunk_documents, load_documents


def _load_corpus() -> list[dict]:
    return chunk_documents(load_documents())


def semantic_search(query: str, top_k: int = 10) -> list[dict]:
    """
    Tìm kiếm ngữ nghĩa dạng local token-vector.

    Returns:
        List of {'content': str, 'score': float, 'metadata': dict}
    """
    if top_k <= 0:
        return []
    return score_chunks(query, _load_corpus(), top_k=top_k)


if __name__ == "__main__":
    for result in semantic_search("hình phạt cho tội tàng trữ ma tuý", top_k=5):
        print(f"[{result['score']:.3f}] {result['content'][:100]}...")
