"""Integration boundary for the group RAG pipeline.

Protected file: only change this after coordinating with the team.
Most implementation work should happen in `retrieval.py` and `generation.py`.
"""

from __future__ import annotations

from .generation import generate_with_citation
from .retrieval import retrieve
from .utils import RAGResponse, normalize_history


def generate_answer(
    question: str,
    history: list[dict] | None = None,
    top_k: int = 5,
    use_reranking: bool = True,
) -> RAGResponse:
    """
    Return the stable response shape expected by the group chat UI.

    Required output:
    - answer: cited answer string
    - sources: source documents used
    - history: conversation history
    - question: current user question
    """
    normalized_history = normalize_history(history)
    sources = retrieve(question, top_k=top_k, use_reranking=use_reranking)
    answer = generate_with_citation(question, sources)

    return {
        "answer": answer,
        "sources": sources,
        "history": normalized_history,
        "question": question,
    }
