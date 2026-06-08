"""
Task 9 — Retrieval Pipeline hoàn chỉnh.

Luồng:
    query
      ├─ semantic_search (TF-IDF)         ─┐
      │                                    ├─ gộp bằng RRF → rerank → 'hybrid'
      ├─ lexical_search  (BM25)           ─┘
      └─ nếu điểm tốt nhất < ngưỡng (hoặc rỗng) → fallback pageindex_search

Mỗi kết quả trả về có khoá 'source' ∈ {'hybrid', 'pageindex'}.
"""

from __future__ import annotations

from src.rag_core import rrf_merge
from src.task5_semantic_search import semantic_search
from src.task6_lexical_search import lexical_search
from src.task7_reranking import rerank
from src.task8_pageindex_vectorless import pageindex_search


def _gather_hybrid(query: str, pool_size: int) -> list[dict]:
    """Lấy semantic + lexical rồi hợp nhất bằng Reciprocal Rank Fusion."""
    semantic_hits = semantic_search(query, top_k=pool_size)
    lexical_hits = lexical_search(query, top_k=pool_size)

    by_key: dict[str, dict] = {}
    semantic_ranking, lexical_ranking = [], []
    for hit in semantic_hits:
        key = hit["content"]
        by_key.setdefault(key, hit)
        semantic_ranking.append(key)
    for hit in lexical_hits:
        key = hit["content"]
        by_key.setdefault(key, hit)
        lexical_ranking.append(key)

    fused = rrf_merge([semantic_ranking, lexical_ranking])
    merged = []
    for key, fusion_score in fused:
        item = dict(by_key[key])
        item["score"] = float(fusion_score)
        merged.append(item)
    return merged


def retrieve(
    query: str,
    top_k: int = 5,
    score_threshold: float = 0.3,
    use_reranking: bool = True,
) -> list[dict]:
    """
    Truy hồi hybrid + fallback.

    1. semantic + lexical → RRF.
    2. rerank (nếu bật).
    3. nếu rỗng hoặc điểm cao nhất < score_threshold → fallback PageIndex.
    4. trả về tối đa top_k kết quả, gắn 'source'.
    """
    if top_k <= 0:
        return []

    candidates = _gather_hybrid(query, pool_size=max(top_k * 2, 10))
    if use_reranking and candidates:
        candidates = rerank(query, candidates, top_k=max(top_k, 5))
    for item in candidates:
        item["source"] = "hybrid"

    best_score = candidates[0]["score"] if candidates else 0.0
    if not candidates or best_score < score_threshold:
        fallback = pageindex_search(query, top_k=top_k)
        if fallback:
            return fallback[:top_k]

    return candidates[:top_k]


if __name__ == "__main__":
    for hit in retrieve("hình phạt cho tội mua bán trái phép chất ma tuý", top_k=4):
        print(f"[{hit['score']:.4f}] ({hit['source']}) {hit['content'][:70]}...")
