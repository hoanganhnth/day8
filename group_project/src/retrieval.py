"""Retrieval layer for the group RAG pipeline.

Owner branch: `feature/retrieval-pipeline`.

Expected responsibilities:
- load standardized data selected by the group
- chunk/index documents
- run semantic search
- run lexical/BM25 search
- merge as hybrid retrieval
- apply retrieval fallback when needed
"""

from __future__ import annotations

from .utils import SourceDocument


def retrieve(
    question: str,
    top_k: int = 5,
    use_reranking: bool = True,
) -> list[SourceDocument]:
    """
    Return source documents relevant to the question.

    This scaffold intentionally returns an empty list until the retrieval owner
    integrates the selected implementation from individual submissions.
    """
    _ = question, top_k, use_reranking
    return []
