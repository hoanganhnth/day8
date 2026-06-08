"""
Task 6 — Lexical Search Module (BM25).

BM25 được implement trực tiếp để bài chạy offline:
    score(q,d) = sum(IDF(term) * tf_part * length_norm)
"""

from __future__ import annotations

import math
from collections import Counter

from src.retrieval_utils import tokenize
from src.task4_chunking_indexing import chunk_documents, load_documents

K1 = 1.5
B = 0.75

_CORPUS: list[dict] | None = None
_TOKENIZED: list[list[str]] | None = None
_DOC_FREQ: Counter | None = None
_AVG_DOC_LEN: float = 0.0


def _prepare_index() -> tuple[list[dict], list[list[str]], Counter, float]:
    global _CORPUS, _TOKENIZED, _DOC_FREQ, _AVG_DOC_LEN

    if _CORPUS is None or _TOKENIZED is None or _DOC_FREQ is None:
        _CORPUS = chunk_documents(load_documents())
        _TOKENIZED = [tokenize(doc["content"]) for doc in _CORPUS]
        _DOC_FREQ = Counter()
        for tokens in _TOKENIZED:
            _DOC_FREQ.update(set(tokens))
        _AVG_DOC_LEN = (
            sum(len(tokens) for tokens in _TOKENIZED) / len(_TOKENIZED)
            if _TOKENIZED
            else 0.0
        )

    return _CORPUS, _TOKENIZED, _DOC_FREQ, _AVG_DOC_LEN


def _bm25_score(
    query_tokens: list[str],
    doc_tokens: list[str],
    doc_freq: Counter,
    avg_doc_len: float,
    total_docs: int,
) -> float:
    if not query_tokens or not doc_tokens or avg_doc_len == 0:
        return 0.0

    term_freq = Counter(doc_tokens)
    doc_len = len(doc_tokens)
    score = 0.0

    for term in query_tokens:
        tf = term_freq.get(term, 0)
        if tf == 0:
            continue
        df = doc_freq.get(term, 0)
        idf = math.log(1 + (total_docs - df + 0.5) / (df + 0.5))
        denominator = tf + K1 * (1 - B + B * doc_len / avg_doc_len)
        score += idf * (tf * (K1 + 1)) / denominator

    return float(score)


def lexical_search(query: str, top_k: int = 10) -> list[dict]:
    """
    Tìm kiếm từ khóa sử dụng BM25.

    Returns:
        List of {'content': str, 'score': float, 'metadata': dict}
    """
    if top_k <= 0:
        return []

    corpus, tokenized, doc_freq, avg_doc_len = _prepare_index()
    query_tokens = tokenize(query)
    total_docs = len(corpus)

    results = []
    for doc, doc_tokens in zip(corpus, tokenized):
        results.append(
            {
                "content": doc["content"],
                "score": _bm25_score(
                    query_tokens,
                    doc_tokens,
                    doc_freq,
                    avg_doc_len,
                    total_docs,
                ),
                "metadata": doc.get("metadata", {}),
            }
        )

    results.sort(key=lambda item: item["score"], reverse=True)
    return results[:top_k]


if __name__ == "__main__":
    for result in lexical_search("Điều 248 tàng trữ trái phép chất ma tuý", top_k=5):
        print(f"[{result['score']:.3f}] {result['content'][:100]}...")
