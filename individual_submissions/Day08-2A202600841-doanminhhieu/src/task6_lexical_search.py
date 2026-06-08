"""
Task 6 — Lexical Search (BM25).

Ưu tiên dùng thư viện `rank-bm25` (BM25Okapi) nếu đã cài; nếu không có thì tự
động rơi về BM25Index thuần Python trong rag_core (cùng công thức Okapi). Nhờ
vậy module luôn chạy được, kết quả tương đương.
"""

from __future__ import annotations

from src.rag_core import (
    DEFAULT_CHUNK_OVERLAP,
    DEFAULT_CHUNK_SIZE,
    BM25Index,
    build_corpus,
    vi_tokenize,
)

try:
    from rank_bm25 import BM25Okapi  # type: ignore

    _HAS_RANK_BM25 = True
except Exception:  # pragma: no cover - tùy môi trường
    _HAS_RANK_BM25 = False

_model = None
_chunks: list[dict] | None = None


def _ensure_model():
    global _model, _chunks
    if _model is None:
        _chunks = build_corpus(DEFAULT_CHUNK_SIZE, DEFAULT_CHUNK_OVERLAP)
        tokenized = [vi_tokenize(chunk["content"]) for chunk in _chunks]
        _model = BM25Okapi(tokenized) if _HAS_RANK_BM25 else BM25Index(tokenized)
    return _model, _chunks


def lexical_search(query: str, top_k: int = 10) -> list[dict]:
    """
    Tìm kiếm từ khoá bằng BM25.

    Returns:
        list[{'content': str, 'score': float, 'metadata': dict}] sắp xếp giảm dần.
    """
    if top_k <= 0:
        return []
    model, chunks = _ensure_model()
    query_tokens = vi_tokenize(query)
    if _HAS_RANK_BM25:
        scores = list(model.get_scores(query_tokens))
    else:
        scores = model.scores(query_tokens)
    order = sorted(range(len(chunks)), key=lambda i: scores[i], reverse=True)[:top_k]
    return [
        {"content": chunks[i]["content"], "score": float(scores[i]), "metadata": chunks[i]["metadata"]}
        for i in order
    ]


if __name__ == "__main__":
    engine = "rank-bm25" if _HAS_RANK_BM25 else "BM25 thuần Python"
    print(f"(engine: {engine})")
    for hit in lexical_search("tàng trữ trái phép chất ma tuý", top_k=5):
        print(f"[{hit['score']:.4f}] {hit['metadata'].get('source')} :: {hit['content'][:80]}...")
