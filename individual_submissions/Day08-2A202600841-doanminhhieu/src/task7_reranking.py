"""
Task 7 — Reranking.

Chọn cách MMR-lite kết hợp độ liên quan từ khoá: chấm lại mỗi ứng viên bằng
mức trùng token với truy vấn (đã chuẩn hoá theo độ dài), rồi pha với điểm gốc
của tầng retrieval. Cách này không cần model nặng, vẫn đẩy được tài liệu sát
truy vấn lên trên và giảm phụ thuộc vào điểm thô ban đầu.

Để sẵn cửa cắm cross-encoder thật (jina-reranker / Qwen3-Reranker) qua API —
xem hàm `_cross_encoder_scores` (mặc định trả None để dùng cơ chế local).
"""

from __future__ import annotations

import math

from src.rag_core import vi_tokenize

# Trọng số pha giữa độ liên quan từ khoá và điểm gốc.
_RELEVANCE_WEIGHT = 0.7
_PRIOR_WEIGHT = 0.3


def _cross_encoder_scores(query, documents):  # pragma: no cover - cửa cắm API
    """Trả về list điểm nếu dùng reranker thật; mặc định None (dùng local)."""
    return None


def _keyword_relevance(query_tokens: set, content: str) -> float:
    tokens = vi_tokenize(content)
    if not tokens:
        return 0.0
    overlap = sum(1 for token in tokens if token in query_tokens)
    # Chuẩn hoá theo log độ dài để đoạn dài không bị thiên vị.
    return overlap / math.log(2 + len(tokens))


def rerank(query: str, candidates: list[dict], top_k: int = 5) -> list[dict]:
    """
    Chấm lại và sắp xếp lại danh sách ứng viên theo độ liên quan với query.

    Returns:
        list[dict] đã re-sort, mỗi phần tử có 'score' (điểm rerank mới).
    """
    if not candidates:
        return []

    external = _cross_encoder_scores(query, [c.get("content", "") for c in candidates])
    query_tokens = set(vi_tokenize(query))

    reranked = []
    for position, candidate in enumerate(candidates):
        if external is not None:
            new_score = float(external[position])
        else:
            relevance = _keyword_relevance(query_tokens, candidate.get("content", ""))
            prior = float(candidate.get("score", 0.0))
            new_score = _RELEVANCE_WEIGHT * relevance + _PRIOR_WEIGHT * prior
        item = dict(candidate)
        item["score"] = new_score
        item["rerank_score"] = new_score
        reranked.append(item)

    reranked.sort(key=lambda x: x["score"], reverse=True)
    return reranked[:top_k]


if __name__ == "__main__":
    demo = [
        {"content": "Tội tàng trữ trái phép chất ma tuý bị phạt tù", "score": 0.6, "metadata": {}},
        {"content": "Một bài báo về bóng đá", "score": 0.9, "metadata": {}},
    ]
    for hit in rerank("hình phạt tàng trữ ma tuý", demo, top_k=2):
        print(f"[{hit['score']:.4f}] {hit['content'][:60]}")
