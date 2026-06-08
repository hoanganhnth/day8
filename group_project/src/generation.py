"""Generation and citation formatting for the group RAG pipeline.

Owner branch: `feature/generation-citation`.
"""

from __future__ import annotations

from .utils import NOT_INTEGRATED_MESSAGE, SourceDocument


def generate_with_citation(question: str, sources: list[SourceDocument]) -> str:
    """
    Generate a cited answer from retrieved source documents.

    Replace this scaffold with the selected generation strategy. The final
    answer must cite source documents and refuse unsupported claims.
    """
    _ = question
    if not sources:
        return NOT_INTEGRATED_MESSAGE

    answer_parts = []
    for source in sources[:3]:
        metadata = source.get("metadata", {})
        label = metadata.get("source", source.get("source", "source"))
        content = source.get("content", "").strip()
        if content:
            answer_parts.append(f"{content[:240]} [{label}]")

    return " ".join(answer_parts) if answer_parts else NOT_INTEGRATED_MESSAGE
