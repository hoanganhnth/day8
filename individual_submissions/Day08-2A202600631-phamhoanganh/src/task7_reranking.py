"""
Task 7 — Reranking Module.

Local reranker dùng token cosine similarity, kèm MMR và RRF. Cách này đủ ổn
cho lab offline và vẫn minh họa đúng vai trò reranking: chấm lại relevance và
gộp kết quả từ nhiều retriever.
"""

from __future__ import annotations

from collections import Counter

from src.retrieval_utils import cosine_from_counters, tokenize


def _as_counter(value) -> Counter:
    if isinstance(value, Counter):
        return value
    if isinstance(value, dict):
        return Counter(value)
    if isinstance(value, str):
        return Counter(tokenize(value))
    if isinstance(value, list):
        return Counter(value)
    return Counter()


def rerank_cross_encoder(
    query: str,
    candidates: list[dict],
    top_k: int = 5,
) -> list[dict]:
    """
    Local cross-encoder-style fallback: score each candidate against query text.
    """
    query_counts = Counter(tokenize(query))
    rescored: list[dict] = []

    for candidate in candidates:
        doc_counts = Counter(tokenize(candidate.get("content", "")))
        similarity = cosine_from_counters(query_counts, doc_counts)
        original = float(candidate.get("score", 0.0))
        item = candidate.copy()
        item["score"] = float(0.75 * similarity + 0.25 * original)
        rescored.append(item)

    rescored.sort(key=lambda item: item["score"], reverse=True)
    return rescored[: max(top_k, 0)]


def rerank_mmr(
    query_embedding,
    candidates: list[dict],
    top_k: int = 5,
    lambda_param: float = 0.7,
) -> list[dict]:
    """
    Maximal Marginal Relevance: chọn kết quả vừa relevant vừa ít trùng lặp.
    """
    if not candidates or top_k <= 0:
        return []

    query_counts = _as_counter(query_embedding)
    doc_counts = [
        _as_counter(candidate.get("embedding")) or Counter(tokenize(candidate.get("content", "")))
        for candidate in candidates
    ]

    selected: list[int] = []
    remaining = set(range(len(candidates)))

    while remaining and len(selected) < top_k:
        best_idx = None
        best_score = float("-inf")

        for idx in remaining:
            relevance = cosine_from_counters(query_counts, doc_counts[idx])
            diversity_penalty = 0.0
            if selected:
                diversity_penalty = max(
                    cosine_from_counters(doc_counts[idx], doc_counts[chosen])
                    for chosen in selected
                )
            mmr_score = lambda_param * relevance - (1 - lambda_param) * diversity_penalty
            if mmr_score > best_score:
                best_idx = idx
                best_score = mmr_score

        if best_idx is None:
            break
        selected.append(best_idx)
        remaining.remove(best_idx)

    results = []
    for idx in selected:
        item = candidates[idx].copy()
        item["score"] = float(cosine_from_counters(query_counts, doc_counts[idx]))
        results.append(item)
    return results


def rerank_rrf(
    ranked_lists: list[list[dict]],
    top_k: int = 5,
    k: int = 60,
) -> list[dict]:
    """
    Reciprocal Rank Fusion.
    """
    scores: dict[str, float] = {}
    items: dict[str, dict] = {}

    for ranked_list in ranked_lists:
        for rank, item in enumerate(ranked_list, start=1):
            key = item.get("content", "")
            if not key:
                continue
            scores[key] = scores.get(key, 0.0) + 1.0 / (k + rank)
            items.setdefault(key, item.copy())

    fused = []
    for content, score in sorted(scores.items(), key=lambda pair: pair[1], reverse=True):
        item = items[content]
        item["score"] = float(score)
        fused.append(item)

    return fused[: max(top_k, 0)]


def rerank(
    query: str,
    candidates: list[dict],
    top_k: int = 5,
    method: str = "cross_encoder",
) -> list[dict]:
    """
    Unified reranking interface.
    """
    if top_k <= 0:
        return []
    if not candidates:
        return []

    if method == "cross_encoder":
        return rerank_cross_encoder(query, candidates, top_k)
    if method == "mmr":
        return rerank_mmr(Counter(tokenize(query)), candidates, top_k)
    if method == "rrf":
        if candidates and isinstance(candidates[0], list):
            return rerank_rrf(candidates, top_k)
        return rerank_rrf([candidates], top_k)
    raise ValueError(f"Unknown rerank method: {method}")


if __name__ == "__main__":
    sample = [
        {"content": "Tội tàng trữ ma túy bị xử lý theo Bộ luật Hình sự.", "score": 0.4},
        {"content": "Python programming", "score": 0.8},
    ]
    print(rerank("hình phạt ma túy", sample, top_k=2))
