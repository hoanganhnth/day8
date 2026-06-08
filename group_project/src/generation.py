"""Generation and citation formatting for the group RAG pipeline.

Owner branch: `feature/generation-citation`.
"""

from __future__ import annotations

from .utils import NOT_INTEGRATED_MESSAGE, SourceDocument
from .task10_generation import generate_with_citation as llm_generate


def generate_with_citation(question: str, sources: list[SourceDocument]) -> str:
    """
    Generate a cited answer from retrieved source documents.
    """
    if not sources:
        return NOT_INTEGRATED_MESSAGE

    # Convert SourceDocument to dict for task10_generation
    context_chunks = []
    for s in sources:
        context_chunks.append({
            "content": s.get("content", ""),
            "metadata": s.get("metadata", {}),
            "source": s.get("source", "hybrid")
        })

    # Call the actual generation logic
    result = llm_generate(question, context_chunks)
    return result["answer"]
