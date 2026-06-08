"""
Task 4 — Chunking & Indexing.

Lựa chọn triển khai:
    - Chunking: recursive/paragraph-aware character chunking
    - Chunk size: 500 ký tự, overlap 50 ký tự
    - Embedding/index fallback: local token vectors để bài chạy được offline

Code vẫn giữ cấu trúc RAG pipeline nhưng không phụ thuộc bắt buộc vào ChromaDB
hoặc sentence-transformers trong đường test. Khi cần production/demo nâng cao,
có thể thay `index_to_vectorstore` bằng ChromaDB/FAISS.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from src.retrieval_utils import load_markdown_documents, split_with_overlap, tokenize

STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"
LOCAL_INDEX_PATH = Path(__file__).parent.parent / "data" / "local_index.json"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
CHUNKING_METHOD = "recursive_local"
EMBEDDING_MODEL = "local-token-counts"
EMBEDDING_DIM = 0
VECTOR_STORE = "local-json"
COLLECTION_NAME = "drug_law_docs"


class LocalTokenEmbedder:
    """Tiny embedder-compatible object for local/offline reranking."""

    def encode(self, text_or_texts, **_kwargs):
        def encode_one(text: str) -> dict[str, int]:
            return dict(Counter(tokenize(text)))

        if isinstance(text_or_texts, str):
            return encode_one(text_or_texts)
        return [encode_one(text) for text in text_or_texts]


_embedding_model: LocalTokenEmbedder | None = None


def get_embedding_model() -> LocalTokenEmbedder:
    """Return a lightweight local embedder used by fallback search/rerank."""
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = LocalTokenEmbedder()
    return _embedding_model


def load_documents() -> list[dict]:
    """
    Đọc toàn bộ markdown files từ data/standardized/.

    Returns:
        List of {'content': str, 'metadata': {'source': str, 'type': str}}
    """
    return load_markdown_documents(STANDARDIZED_DIR)


def chunk_documents(documents: list[dict]) -> list[dict]:
    """
    Chunk documents thành các đoạn ổn định, có overlap và metadata rõ ràng.
    """
    chunks: list[dict] = []
    for doc in documents:
        for i, chunk_text in enumerate(
            split_with_overlap(doc["content"], CHUNK_SIZE, CHUNK_OVERLAP)
        ):
            chunks.append(
                {
                    "content": chunk_text,
                    "metadata": {
                        **doc.get("metadata", {}),
                        "chunk_index": i,
                    },
                }
            )
    return chunks


def embed_chunks(chunks: list[dict]) -> list[dict]:
    """Attach local token-count embeddings to chunks."""
    model = get_embedding_model()
    embeddings = model.encode([chunk["content"] for chunk in chunks])
    for chunk, embedding in zip(chunks, embeddings):
        chunk["embedding"] = embedding
    return chunks


def index_to_vectorstore(chunks: list[dict]) -> None:
    """
    Persist a small local JSON index.

    This keeps the lab reproducible without Docker/network setup while matching
    the vector-store step conceptually: chunks + metadata + embedding payload.
    """
    LOCAL_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOCAL_INDEX_PATH.write_text(
        json.dumps(chunks, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"  Indexed {len(chunks)} chunks to {LOCAL_INDEX_PATH}")


def run_pipeline() -> None:
    """Chạy toàn bộ pipeline: load -> chunk -> embed -> local index."""
    docs = load_documents()
    chunks = chunk_documents(docs)
    indexed_chunks = embed_chunks(chunks)
    index_to_vectorstore(indexed_chunks)
    print(
        f"Loaded {len(docs)} documents, created {len(chunks)} chunks "
        f"with {CHUNKING_METHOD}."
    )


if __name__ == "__main__":
    run_pipeline()
