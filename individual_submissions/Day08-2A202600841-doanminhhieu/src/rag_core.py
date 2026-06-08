"""
rag_core — lõi dùng chung cho pipeline RAG.
Tác giả: Đoàn Minh Hiếu (2A202600841).

Triết lý: viết thuần Python, không phụ thuộc thư viện nặng để pipeline luôn
chạy được; nhưng để sẵn "cửa" cắm thư viện thật (rank-bm25, sentence-transformers)
khi môi trường có cài. Toàn bộ retrieval xoay quanh:

  * vi_tokenize   — tách từ tiếng Việt/anh, bỏ stopword.
  * TfidfIndex    — vector hoá TF-IDF + cosine (dùng cho semantic search).
  * BM25Index     — Okapi BM25 tự cài (dùng cho lexical search).
  * rrf_merge     — Reciprocal Rank Fusion để gộp nhiều bảng xếp hạng.
  * build_corpus  — đọc data/standardized/**.md rồi cắt chunk (cache lại).
"""

from __future__ import annotations

import math
import re
from collections import Counter, defaultdict
from pathlib import Path

# --- Vị trí dữ liệu chuẩn hoá ------------------------------------------------
_PKG_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = _PKG_ROOT / "data"
STANDARDIZED_DIR = DATA_DIR / "standardized"

# Tham số chunk mặc định (task4 tái sử dụng để giữ nhất quán toàn pipeline).
DEFAULT_CHUNK_SIZE = 800
DEFAULT_CHUNK_OVERLAP = 120

# Stopword tiếng Việt tối giản — giảm nhiễu khi tính độ tương đồng.
_STOPWORDS = {
    "và", "của", "các", "có", "được", "cho", "trong", "là", "với", "để",
    "này", "đó", "khi", "về", "theo", "tại", "một", "những", "đã", "bị",
    "the", "a", "an", "of", "to", "in", "is", "for", "on", "and",
}
_TOKEN_PATTERN = re.compile(r"\w+", re.UNICODE)


def vi_tokenize(text: str) -> list[str]:
    """Tách token, hạ chữ thường, loại stopword và token 1 ký tự rời."""
    raw = _TOKEN_PATTERN.findall((text or "").lower())
    return [t for t in raw if t not in _STOPWORDS and (len(t) > 1 or t.isdigit())]


class TfidfIndex:
    """Chỉ mục TF-IDF + cosine similarity cho dense-like semantic search."""

    def __init__(self, corpus_tokens: list[list[str]]):
        self.size = len(corpus_tokens)
        doc_freq: Counter = Counter()
        for tokens in corpus_tokens:
            for term in set(tokens):
                doc_freq[term] += 1
        # IDF làm trơn (smooth) để tránh chia 0.
        self.idf = {
            term: math.log((1 + self.size) / (1 + freq)) + 1.0
            for term, freq in doc_freq.items()
        }
        self._vectors = [self._to_vector(tokens) for tokens in corpus_tokens]
        self._norms = [math.sqrt(sum(w * w for w in v.values())) for v in self._vectors]

    def _to_vector(self, tokens: list[str]) -> dict[str, float]:
        counts = Counter(tokens)
        return {term: freq * self.idf.get(term, 0.0) for term, freq in counts.items()}

    def rank(self, query_tokens: list[str], top_k: int) -> list[tuple[int, float]]:
        q_vec = self._to_vector(query_tokens)
        q_norm = math.sqrt(sum(w * w for w in q_vec.values()))
        scores = []
        for i, (vec, norm) in enumerate(zip(self._vectors, self._norms)):
            if q_norm == 0 or norm == 0:
                scores.append(0.0)
                continue
            dot = sum(weight * vec.get(term, 0.0) for term, weight in q_vec.items())
            scores.append(dot / (q_norm * norm))
        order = sorted(range(self.size), key=lambda i: scores[i], reverse=True)
        return [(i, scores[i]) for i in order[:top_k]]


class BM25Index:
    """Okapi BM25 tự cài (k1, b mặc định theo tài liệu chuẩn)."""

    def __init__(self, corpus_tokens: list[list[str]], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.corpus_tokens = corpus_tokens
        self.size = len(corpus_tokens)
        self.doc_len = [len(tokens) for tokens in corpus_tokens]
        self.avg_len = (sum(self.doc_len) / self.size) if self.size else 0.0
        self._tf = [Counter(tokens) for tokens in corpus_tokens]
        doc_freq: Counter = Counter()
        for tokens in corpus_tokens:
            for term in set(tokens):
                doc_freq[term] += 1
        self.idf = {
            term: math.log(1 + (self.size - freq + 0.5) / (freq + 0.5))
            for term, freq in doc_freq.items()
        }

    def scores(self, query_tokens: list[str]) -> list[float]:
        out = []
        for i in range(self.size):
            tf, dl = self._tf[i], self.doc_len[i]
            s = 0.0
            for term in query_tokens:
                freq = tf.get(term, 0)
                if not freq:
                    continue
                denom = freq + self.k1 * (1 - self.b + self.b * dl / (self.avg_len or 1))
                s += self.idf.get(term, 0.0) * (freq * (self.k1 + 1)) / denom
            out.append(s)
        return out


def rrf_merge(ranked_keys: list[list], k: int = 60) -> list[tuple]:
    """Reciprocal Rank Fusion: gộp nhiều danh sách đã xếp hạng thành một."""
    fused: dict = defaultdict(float)
    for ranking in ranked_keys:
        for position, key in enumerate(ranking):
            fused[key] += 1.0 / (k + position + 1)
    return sorted(fused.items(), key=lambda kv: kv[1], reverse=True)


def split_text(text: str, size: int, overlap: int) -> list[str]:
    """Cắt văn bản thành đoạn <= size, ưu tiên ngắt ở ranh giới đoạn/câu."""
    text = re.sub(r"\n{3,}", "\n\n", (text or "").strip())
    if not text:
        return []
    if len(text) <= size:
        return [text]
    chunks: list[str] = []
    start, n = 0, len(text)
    while start < n:
        end = min(start + size, n)
        if end < n:
            window = text[start:end]
            boundary = max(window.rfind("\n\n"), window.rfind("\n"), window.rfind(". "))
            if boundary > size * 0.5:
                end = start + boundary + 1
        piece = text[start:end].strip()
        if piece:
            chunks.append(piece)
        if end >= n:
            break
        start = max(end - overlap, start + 1)
    return chunks


def load_standardized_documents() -> list[dict]:
    """Đọc toàn bộ markdown đã chuẩn hoá thành list document dict."""
    documents: list[dict] = []
    for category in ("legal", "news"):
        folder = STANDARDIZED_DIR / category
        if not folder.exists():
            continue
        for path in sorted(folder.glob("*.md")):
            documents.append(
                {
                    "content": path.read_text(encoding="utf-8"),
                    "metadata": {"source": path.name, "type": category, "path": str(path)},
                }
            )
    return documents


_CORPUS_CACHE: dict = {}


def build_corpus(size: int = DEFAULT_CHUNK_SIZE, overlap: int = DEFAULT_CHUNK_OVERLAP) -> list[dict]:
    """Đọc + cắt chunk toàn bộ tài liệu (có cache theo cấu hình size/overlap)."""
    cache_key = (size, overlap)
    if cache_key in _CORPUS_CACHE:
        return _CORPUS_CACHE[cache_key]
    chunks: list[dict] = []
    for document in load_standardized_documents():
        for index, piece in enumerate(split_text(document["content"], size, overlap)):
            meta = dict(document["metadata"])
            meta["chunk_id"] = index
            chunks.append({"content": piece, "score": 0.0, "metadata": meta})
    _CORPUS_CACHE[cache_key] = chunks
    return chunks
