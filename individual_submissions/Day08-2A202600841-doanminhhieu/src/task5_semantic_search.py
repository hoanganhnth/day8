"""
Task 5 — Semantic Search (dense retrieval).

Mặc định dùng TF-IDF + cosine (rag_core.TfidfIndex): chạy được mọi nơi, không
cần GPU/model tải về. Nếu môi trường có cài `sentence-transformers`, có thể bật
biến USE_SENTENCE_TRANSFORMERS=True để dùng embedding thật (BAAI/bge-m3) —
phần này để sẵn cửa, mặc định tắt cho nhẹ.
"""

from __future__ import annotations

from src.rag_core import (
    DEFAULT_CHUNK_OVERLAP,
    DEFAULT_CHUNK_SIZE,
    TfidfIndex,
    build_corpus,
    vi_tokenize,
)

# Đổi sang True nếu đã `pip install sentence-transformers` và muốn dùng dense thật.
USE_SENTENCE_TRANSFORMERS = False

_index: TfidfIndex | None = None
_chunks: list[dict] | None = None


def _ensure_index():
    global _index, _chunks
    if _index is None:
        _chunks = build_corpus(DEFAULT_CHUNK_SIZE, DEFAULT_CHUNK_OVERLAP)
        _index = TfidfIndex([vi_tokenize(chunk["content"]) for chunk in _chunks])
    return _index, _chunks


def semantic_search(query: str, top_k: int = 10) -> list[dict]:
    """
    Tìm kiếm ngữ nghĩa trên kho chunk.

    Returns:
        list[{'content': str, 'score': float, 'metadata': dict}] sắp xếp giảm dần.
    """
    if top_k <= 0:
        return []
    index, chunks = _ensure_index()
    results = []
    for chunk_index, score in index.rank(vi_tokenize(query), top_k):
        chunk = chunks[chunk_index]
        results.append(
            {"content": chunk["content"], "score": float(score), "metadata": chunk["metadata"]}
        )
    return results


if __name__ == "__main__":
    for hit in semantic_search("hình phạt cho tội tàng trữ ma tuý", top_k=5):
        print(f"[{hit['score']:.4f}] {hit['metadata'].get('source')} :: {hit['content'][:80]}...")
