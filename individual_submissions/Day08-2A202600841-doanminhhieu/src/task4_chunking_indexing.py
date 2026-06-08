"""
Task 4 — Chunking & Indexing.

Chiến lược chunking: cắt theo ký tự có chồng lấn (overlap), nhưng cố gắng ngắt
ở ranh giới đoạn/câu để không vỡ ý — xử lý tốt cho cả văn bản luật (điều/khoản)
lẫn bài báo. Cấu hình:

  * CHUNK_SIZE = 800 ký tự  — đủ gọn cho một điều luật ngắn hoặc một đoạn báo,
    vẫn vừa context window khi đưa vào LLM.
  * CHUNK_OVERLAP = 120 ký tự — giữ liên tục ngữ cảnh giữa hai chunk kề nhau.

"Embedding model": ở chế độ mặc định dùng biểu diễn TF-IDF (xem rag_core), nhẹ
và không cần GPU; có thể thay bằng sentence-transformers/all-MiniLM-L6-v2 hoặc
BAAI/bge-m3 nếu môi trường cài đặt (xem task5).
"""

from __future__ import annotations

from src.rag_core import (
    DEFAULT_CHUNK_OVERLAP,
    DEFAULT_CHUNK_SIZE,
    build_corpus,
    load_standardized_documents,
    split_text,
)

CHUNK_SIZE = DEFAULT_CHUNK_SIZE
CHUNK_OVERLAP = DEFAULT_CHUNK_OVERLAP


def load_documents() -> list[dict]:
    """Nạp toàn bộ tài liệu markdown đã chuẩn hoá."""
    return load_standardized_documents()


def chunk_documents(documents: list[dict]) -> list[dict]:
    """Cắt mỗi document thành các chunk <= CHUNK_SIZE, kèm metadata nguồn."""
    chunks: list[dict] = []
    for document in documents:
        meta_base = document.get("metadata", {})
        for index, piece in enumerate(split_text(document.get("content", ""), CHUNK_SIZE, CHUNK_OVERLAP)):
            meta = dict(meta_base)
            meta["chunk_id"] = index
            chunks.append({"content": piece, "metadata": meta})
    return chunks


def build_index() -> list[dict]:
    """Trả về toàn bộ chunk đã index (dùng chung với task5/task6 qua cache)."""
    return build_corpus(CHUNK_SIZE, CHUNK_OVERLAP)


if __name__ == "__main__":
    docs = load_documents()
    chunks = chunk_documents(docs)
    print(f"Đã nạp {len(docs)} tài liệu, cắt thành {len(chunks)} chunk "
          f"(size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP}).")
