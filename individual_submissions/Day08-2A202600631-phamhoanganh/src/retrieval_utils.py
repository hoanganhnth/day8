"""Small local retrieval helpers used when optional RAG libraries are absent."""

from __future__ import annotations

import math
import re
from collections import Counter
from pathlib import Path


TOKEN_RE = re.compile(r"\w+", re.UNICODE)


def tokenize(text: str) -> list[str]:
    """Tokenize Vietnamese/English text with a dependency-free regex."""
    return TOKEN_RE.findall(text.lower())


def cosine_from_counters(query_counts: Counter, doc_counts: Counter) -> float:
    """Cosine similarity over sparse token-count vectors."""
    if not query_counts or not doc_counts:
        return 0.0

    dot = sum(query_counts[token] * doc_counts.get(token, 0) for token in query_counts)
    query_norm = math.sqrt(sum(value * value for value in query_counts.values()))
    doc_norm = math.sqrt(sum(value * value for value in doc_counts.values()))
    if query_norm == 0 or doc_norm == 0:
        return 0.0
    return float(dot / (query_norm * doc_norm))


def split_with_overlap(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    """Split text into stable character chunks with paragraph-aware boundaries."""
    clean_text = re.sub(r"\n{3,}", "\n\n", text.strip())
    if not clean_text:
        return []
    if len(clean_text) <= chunk_size:
        return [clean_text]

    chunks: list[str] = []
    start = 0
    min_step = max(1, chunk_size - chunk_overlap)

    while start < len(clean_text):
        hard_end = min(len(clean_text), start + chunk_size)
        end = hard_end

        if hard_end < len(clean_text):
            window = clean_text[start:hard_end]
            boundary_candidates = [
                window.rfind("\n\n"),
                window.rfind("\n"),
                window.rfind(". "),
                window.rfind(" "),
            ]
            best = max(boundary_candidates)
            if best >= int(chunk_size * 0.55):
                end = start + best + 1

        chunk = clean_text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= len(clean_text):
            break
        start = max(end - chunk_overlap, start + min_step)

    return chunks


def load_markdown_documents(base_dir: Path) -> list[dict]:
    """Load markdown files from data/standardized into document dictionaries."""
    documents: list[dict] = []
    if not base_dir.exists():
        return documents

    for md_file in sorted(base_dir.rglob("*.md")):
        content = md_file.read_text(encoding="utf-8").strip()
        if len(content) < 50:
            continue
        rel_path = md_file.relative_to(base_dir)
        doc_type = rel_path.parts[0] if len(rel_path.parts) > 1 else "unknown"
        documents.append(
            {
                "content": content,
                "metadata": {
                    "source": md_file.name,
                    "path": str(rel_path),
                    "type": doc_type,
                },
            }
        )
    return documents


def score_chunks(query: str, chunks: list[dict], top_k: int = 10) -> list[dict]:
    """Dependency-free semantic-ish search over chunks using token cosine."""
    query_counts = Counter(tokenize(query))
    scored: list[dict] = []

    for chunk in chunks:
        content = chunk.get("content", "")
        doc_counts = Counter(tokenize(content))
        score = cosine_from_counters(query_counts, doc_counts)
        scored.append(
            {
                "content": content,
                "score": score,
                "metadata": chunk.get("metadata", {}),
            }
        )

    scored.sort(key=lambda item: item["score"], reverse=True)
    return scored[: max(top_k, 0)]
