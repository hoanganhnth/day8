"""Shared data shapes and helpers for the group RAG project."""

from __future__ import annotations

from typing import TypedDict


class SourceDocument(TypedDict, total=False):
    content: str
    score: float
    source: str
    metadata: dict


class RAGResponse(TypedDict):
    answer: str
    sources: list[SourceDocument]
    history: list[dict]
    question: str


NOT_INTEGRATED_MESSAGE = (
    "Group pipeline chưa được tích hợp. "
    "Hãy hoàn thiện retrieval.py và generation.py theo phân công trong BRANCH_RULES.md."
)


def normalize_history(history: list[dict] | None) -> list[dict]:
    return list(history or [])
