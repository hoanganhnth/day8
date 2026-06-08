import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

def reorder_for_llm(chunks: list[dict]) -> list[dict]:
    if not chunks:
        return []
    reordered = [None] * len(chunks)
    left, right = 0, len(chunks) - 1
    for i, chunk in enumerate(chunks):
        if i % 2 == 0:
            reordered[left] = chunk
            left += 1
        else:
            reordered[right] = chunk
            right -= 1
    return reordered

def format_context(chunks: list[dict]) -> str:
    ctx = ""
    for i, chunk in enumerate(chunks):
        src = chunk.get("metadata", {}).get("source", f"doc_{i}")
        if src.endswith(".pdf") or src.endswith(".md"):
            src = src.rsplit(".", 1)[0]
        ctx += f"[{src}] {chunk.get('content', '')}\n\n"
    return ctx

def generate_with_citation(query: str, context_chunks: list[dict] = None) -> dict:
    if context_chunks is None:
        context_chunks = []
    
    reordered = reorder_for_llm(context_chunks)
    ctx_str = format_context(reordered)
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("WARNING: No OPENAI_API_KEY found, falling back to dummy response.")
        return {
            "answer": f"Based on the context, here is the answer. [Nguồn, 2023]\n\nContext used:\n{ctx_str}",
            "sources": reordered
        }
        
    client = OpenAI(base_url="https://openrouter.ai/api/v1")
    
    prompt = f"""Bạn là một chuyên gia pháp lý và phân tích tin tức.
Dựa vào ngữ cảnh được cung cấp bên dưới, hãy trả lời câu hỏi của người dùng.
Trong câu trả lời, bắt buộc phải trích dẫn nguồn bằng cách sử dụng cú pháp [Tên nguồn].
Nếu ngữ cảnh không chứa thông tin để trả lời, hãy nói rõ là bạn không biết.

NGỮ CẢNH:
{ctx_str}

CÂU HỎI:
{query}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=512
    )
    
    answer = response.choices[0].message.content
    
    return {
        "answer": answer,
        "sources": reordered
    }
