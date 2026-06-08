"""Integration boundary for the group RAG pipeline."""

from __future__ import annotations


def generate_answer(question: str, history: list[dict] | None = None) -> dict:
    """
    Return the stable response shape expected by the group chat UI.

    Replace this scaffold with the selected retrieval and generation modules
    from individual submissions.
    """
    return {
        "answer": (
            "Group pipeline chưa được tích hợp. "
            "Hãy chọn và đưa retrieval/generation từ bài cá nhân vào group_project/src."
        ),
        "sources": [],
        "history": history or [],
        "question": question,
    }
