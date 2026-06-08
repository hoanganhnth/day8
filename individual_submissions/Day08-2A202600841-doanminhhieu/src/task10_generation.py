"""
Task 10 — Generation có Citation.

Ba việc chính:
  1. reorder_for_llm  — xếp lại chunk theo kiểu "quan trọng ở hai đầu" để chống
     hiện tượng *lost in the middle* (Liu et al., 2023).
  2. format_context   — dựng context kèm nhãn nguồn để LLM trích dẫn được.
  3. generate_with_citation — ghép prompt, gọi LLM nếu có API key, nếu không thì
     trả lời trích dẫn theo cách extractive cục bộ (luôn chạy được).

Chọn top_p/temperature thấp (0.2 / 0.9) để câu trả lời pháp luật bám sát ngữ
cảnh, hạn chế "bịa".
"""

from __future__ import annotations

import os
import re

TEMPERATURE = 0.2
TOP_P = 0.9

SYSTEM_PROMPT = (
    "Bạn là trợ lý pháp luật. Trả lời câu hỏi dựa HOÀN TOÀN vào context được cung "
    "cấp. Sau mỗi ý/khẳng định, chèn ngay trích dẫn trong ngoặc vuông trỏ tới nguồn "
    "(ví dụ [luat-phong-chong-ma-tuy-2021.md]). Nếu context không chứa thông tin, "
    "hãy trả lời 'I cannot verify this information' thay vì đoán."
)


def reorder_for_llm(chunks: list[dict]) -> list[dict]:
    """
    Xếp lại theo mẫu xen kẽ rồi gập đôi: chunk quan trọng nhất nằm ở đầu, các
    chunk kém quan trọng dồn vào giữa, vẫn giữ nguyên số lượng.
    Ví dụ thứ tự độ quan trọng [0,1,2,3,4] -> [0,2,4,3,1].
    """
    if not chunks:
        return []
    left, right = [], []
    for index, chunk in enumerate(chunks):
        (left if index % 2 == 0 else right).append(chunk)
    return left + right[::-1]


def _source_of(chunk: dict) -> str:
    meta = chunk.get("metadata") or {}
    return meta.get("source") or chunk.get("source") or "unknown"


def format_context(chunks: list[dict]) -> str:
    """Dựng context có đánh số + nhãn nguồn cho từng đoạn."""
    blocks = []
    for index, chunk in enumerate(chunks, start=1):
        blocks.append(f"[{index}] (Nguồn: {_source_of(chunk)})\n{chunk.get('content', '')}")
    return "\n\n".join(blocks)


def _first_sentences(text: str, max_chars: int = 400) -> str:
    text = re.sub(r"\s+", " ", (text or "").strip())
    if len(text) <= max_chars:
        return text
    cut = text[:max_chars]
    dot = cut.rfind(". ")
    return (cut[: dot + 1] if dot > max_chars * 0.4 else cut).strip()


def call_llm(messages: list[dict]) -> str | None:
    """Gọi LLM thật nếu có OPENAI_API_KEY + thư viện openai; ngược lại None."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    try:  # pragma: no cover - chỉ chạy khi có key
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=messages,
            temperature=TEMPERATURE,
            top_p=TOP_P,
        )
        return response.choices[0].message.content
    except Exception:
        return None


def _extractive_answer(query: str, ranked_chunks: list[dict]) -> str:
    """Trả lời extractive cục bộ khi không có LLM: trích đoạn sát nhất + citation."""
    if not ranked_chunks:
        return "I cannot verify this information"
    top = ranked_chunks[0]
    snippet = _first_sentences(top.get("content", ""), 400)
    return f"{snippet} [{_source_of(top)}]"


def generate_with_citation(query: str, top_k: int = 5, use_reranking: bool = True) -> dict:
    """
    Sinh câu trả lời có trích dẫn.

    Returns:
        dict {'question', 'answer', 'sources', 'context'}
    """
    from src.task9_retrieval_pipeline import retrieve

    ranked = retrieve(query, top_k=top_k, use_reranking=use_reranking)
    ordered = reorder_for_llm(ranked)
    context = format_context(ordered)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Context:\n{context}\n\nCâu hỏi: {query}"},
    ]
    answer = call_llm(messages) or _extractive_answer(query, ranked)

    sources = []
    for chunk in ranked:
        src = _source_of(chunk)
        if src not in sources:
            sources.append(src)

    return {"question": query, "answer": answer, "sources": sources, "context": context}


if __name__ == "__main__":
    result = generate_with_citation("Hình phạt cho tội tàng trữ trái phép chất ma tuý?")
    print("Answer:", result["answer"])
    print("Sources:", result["sources"])
