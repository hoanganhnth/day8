"""
Task 4 — Chunking & Indexing vào Vector Store.

Hướng dẫn:
    1. Đọc toàn bộ markdown files từ data/standardized/
    2. Chọn 1 chunking strategy (giải thích lý do)
    3. Chọn 1 embedding model (giải thích lý do)
    4. Index vào vector store (Weaviate khuyến cáo)

Chunking options (langchain-text-splitters):
    - RecursiveCharacterTextSplitter: an toàn, phổ biến
    - MarkdownHeaderTextSplitter: tốt cho file có heading
    - SemanticChunker: dùng embedding để tách (nâng cao)

Embedding model options:
    - sentence-transformers/all-MiniLM-L6-v2 (384 dim, nhẹ)
    - BAAI/bge-m3 (1024 dim, multilingual, tốt cho tiếng Việt)
    - OpenAI text-embedding-3-small (1536 dim, API)

Vector store options:
    - Weaviate (khuyến cáo: hỗ trợ hybrid search built-in)
    - ChromaDB (đơn giản, local)
    - FAISS (chỉ dense search)

Cài đặt:
    pip install langchain-text-splitters sentence-transformers weaviate-client
"""

from pathlib import Path

STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"


# =============================================================================
# CONFIGURATION — Giải thích lựa chọn của bạn trong comment
# =============================================================================

# =============================================================================
# CONFIGURATION
# =============================================================================
CHUNK_SIZE = 500        # Giữ nguyên
CHUNK_OVERLAP = 50      # Giữ nguyên
CHUNKING_METHOD = "recursive"

# Đổi sang model nhẹ, chạy nhanh trên CPU (theo gợi ý của README)
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM = 384

VECTOR_STORE = "chromadb"


# =============================================================================
# IMPLEMENTATION
# =============================================================================

def load_documents() -> list[dict]:
    documents = []
    # Rglob sẽ đệ quy quét mọi file .md trong thư mục
    for md_file in STANDARDIZED_DIR.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        # Phân loại đây là luật hay báo chí dựa vào tên thư mục
        doc_type = "legal" if "legal" in str(md_file) else "news"
        documents.append({
            "content": content,
            "metadata": {"source": md_file.name, "type": doc_type}
        })
    return documents



def chunk_documents(documents: list[dict]) -> list[dict]:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = []
    for doc in documents:
        splits = splitter.split_text(doc["content"])
        for i, chunk_text in enumerate(splits):
            chunks.append({
                "content": chunk_text,
                "metadata": {**doc["metadata"], "chunk_index": i}
            })
    return chunks

def embed_chunks(chunks: list[dict]) -> list[dict]:
    from sentence_transformers import SentenceTransformer
    
    # Load model (Lần đầu chạy sẽ tải mất khoảng vài phút)
    model = SentenceTransformer(EMBEDDING_MODEL)
    texts = [c["content"] for c in chunks]
    
    # Biến text thành vector
    embeddings = model.encode(texts, show_progress_bar=True)
    
    for chunk, emb in zip(chunks, embeddings):
        chunk["embedding"] = emb.tolist()
    return chunks

def index_to_vectorstore(chunks: list[dict]):
    import chromadb
    
    # Khởi tạo hoặc load ChromaDB từ thư mục không có dấu tiếng Việt
    db_path = "D:/code/chroma_db_cohort2"
    client = chromadb.PersistentClient(path=db_path)
    
    # Lấy collection hoặc tạo mới (tránh dùng delete_collection trên Windows gây lỗi HNSW)
    collection = client.get_or_create_collection(name="drug_law_docs")
    
    # Chuẩn bị dữ liệu để insert
    ids = [f"{c['metadata']['source']}_{c['metadata']['chunk_index']}" for c in chunks]
    embeddings = [c["embedding"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]
    documents = [c["content"] for c in chunks]
    
    # Đưa vào Database
    collection.add(
        ids=ids,
        embeddings=embeddings,
        metadatas=metadatas,
        documents=documents
    )

def run_pipeline():
    """Chạy toàn bộ pipeline: load → chunk → embed → index."""
    print("=" * 50)
    print("Task 4: Chunking & Indexing")
    print(f"  Chunking: {CHUNKING_METHOD} (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")
    print(f"  Embedding: {EMBEDDING_MODEL} (dim={EMBEDDING_DIM})")
    print(f"  Vector Store: {VECTOR_STORE}")
    print("=" * 50)

    docs = load_documents()
    print(f"\n✓ Loaded {len(docs)} documents")

    chunks = chunk_documents(docs)
    print(f"✓ Created {len(chunks)} chunks")

    chunks = embed_chunks(chunks)
    print(f"✓ Embedded {len(chunks)} chunks")

    index_to_vectorstore(chunks)
    print("✓ Indexed to vector store")


if __name__ == "__main__":
    run_pipeline()
