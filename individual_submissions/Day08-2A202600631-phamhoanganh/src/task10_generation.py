"""
Task 10 — Generation Có Citation.

Offline implementation: retrieve evidence, reorder chunks, format context, and
produce an extractive Vietnamese answer with source citations. This keeps the
pipeline testable without API keys while preserving the citation contract.
"""

from __future__ import annotations

import re

from .task9_retrieval_pipeline import retrieve

TOP_K = 5
TOP_P = 0.9
TEMPERATURE = 0.3

SYSTEM_PROMPT = """Trả lời bằng tiếng Việt, chỉ dựa trên context đã truy xuất.
Mỗi ý chính phải kèm citation theo source. Nếu không đủ evidence, nói rõ rằng
không thể xác minh từ nguồn hiện có."""


def reorder_for_llm(chunks: list[dict]) -> list[dict]:
    """
    Sắp xếp chunks để tránh lost-in-the-middle.

    Chunk điểm cao nhất giữ ở đầu; các chunk vị trí lẻ đảo về cuối.
    """
    if len(chunks) <= 2:
        return chunks
    even_indexed = [chunks[i] for i in range(len(chunks)) if i % 2 == 0]
    odd_indexed = [chunks[i] for i in range(len(chunks)) if i % 2 == 1]
    return even_indexed + list(reversed(odd_indexed))


def format_context(chunks: list[dict]) -> str:
    """
    Format chunks thành context string có source label cho citation.
    """
    context_parts = []
    for i, chunk in enumerate(chunks, start=1):
        metadata = chunk.get("metadata", {})
        source = metadata.get("source", f"Source {i}")
        doc_type = metadata.get("type", "unknown")
        context_parts.append(
            f"[Document {i} | Source: {source} | Type: {doc_type}]\n"
            f"{chunk.get('content', '')}\n"
        )
    return "\n---\n".join(context_parts)


def _first_sentence(text: str, max_chars: int = 320) -> str:
    clean = re.sub(r"\s+", " ", text).strip()
    if not clean:
        return ""
    match = re.search(r"(.{80,}?[.!?。])\s", clean)
    if match:
        return match.group(1)[:max_chars].strip()
    return clean[:max_chars].strip()


def call_llm(messages: list[dict], temperature: float = TEMPERATURE, top_p: float = TOP_P) -> str:
    """
    Local generation fallback used for offline lab execution.

    The argument shape mirrors an LLM call so callers can swap in OpenAI/Gemini
    later without changing `generate_with_citation`.
    """
    user_text = messages[-1]["content"] if messages else ""
    return _first_sentence(user_text, max_chars=500) or "Tôi không thể xác minh thông tin này từ nguồn hiện có."


def generate_with_citation(
    query: str,
    top_k: int = TOP_K,
    use_reranking: bool = True,
) -> dict:
    """
    End-to-end RAG generation có citation.

    Returns:
        {'answer': str, 'sources': list[dict], 'retrieval_source': str}
    """
    chunks = retrieve(query, top_k=top_k, use_reranking=use_reranking)
    reordered = reorder_for_llm(chunks)

    if not reordered:
        return {
            "answer": "Tôi không thể xác minh thông tin này từ nguồn hiện có.",
            "sources": [],
            "retrieval_source": "none",
        }

    answer_parts = []
    for chunk in reordered[: min(3, len(reordered))]:
        metadata = chunk.get("metadata", {})
        source = metadata.get("source", "nguồn không rõ")
        evidence = _first_sentence(chunk.get("content", ""))
        if evidence:
            answer_parts.append(f"{evidence} [{source}]")

    answer = " ".join(answer_parts).strip()
    if not answer:
        answer = "Tôi không thể xác minh thông tin này từ nguồn hiện có."

    return {
        "answer": answer,
        "sources": chunks,
        "retrieval_source": chunks[0].get("source", "hybrid") if chunks else "none",
    }


if __name__ == "__main__":
    result = generate_with_citation("Hình phạt tàng trữ ma tuý?")
    print(result["answer"])
