import json
import os
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI
from dotenv import load_dotenv
import faiss
import numpy as np

load_dotenv()

STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"
VECTORSTORE_PATH = Path(__file__).parent.parent / "data" / "vectorstore.json"
FAISS_INDEX_PATH = Path(__file__).parent.parent / "data" / "vectorstore.index"

# =====================================================================
# CẤU HÌNH CHUNKING & INDEXING (Đáp ứng yêu cầu Task 4)
# =====================================================================

# 1. Chunking Strategy:
# Sử dụng RecursiveCharacterTextSplitter vì nó chia văn bản an toàn dựa trên
# các dấu phân cách ngữ nghĩa (đoạn văn, câu, từ). Phù hợp nhất với văn bản 
# Pháp luật (thường chia theo Điều, Khoản) và Báo chí (đoạn văn).
CHUNKING_METHOD = "recursive"

# 2. Chunk Size & Overlap:
# - CHUNK_SIZE = 500 ký tự (~100-150 từ): Độ dài vừa đủ để chứa trọn vẹn 1 
#   điều luật ngắn hoặc 1 đoạn tin tức mà không làm nhiễu mô hình LLM.
# - CHUNK_OVERLAP = 50: Giữ lại 50 ký tự gối lên nhau giữa các chunk để 
#   không bị đứt gãy ngữ cảnh (ví dụ: bị cắt ngang giữa câu).
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# 3. Embedding Model & Dimension:
# - Sử dụng OpenAI 'text-embedding-3-small' (như gợi ý của thầy vì nhóm có API).
# - Dimension = 1536. Model này hiểu Tiếng Việt rất tốt, sinh vector nhanh, 
#   chính xác cao hơn so với các model local như MiniLM.
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIM = 1536

# 4. Vector Store:
# Sử dụng FAISS (như gợi ý Alternative của thầy) vì cấu hình nhẹ nhàng, 
# chạy trực tiếp bằng C++ siêu tốc, không cần cài đặt Docker phức tạp như Weaviate.
VECTOR_STORE = "faiss"

def load_documents() -> list[dict]:
    documents = []
    if not STANDARDIZED_DIR.exists(): return documents
    for md_file in STANDARDIZED_DIR.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        doc_type = "legal" if "legal" in str(md_file) else "news"
        documents.append({
            "content": content,
            "metadata": {"source": md_file.name, "type": doc_type}
        })
    return documents

def chunk_documents(documents: list[dict]) -> list[dict]:
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
    client = OpenAI()
    texts = [chunk["content"] for chunk in chunks]
    print(f"Embedding {len(texts)} chunks via OpenAI API...")
    
    response = client.embeddings.create(input=texts, model=EMBEDDING_MODEL)
    
    for i, chunk in enumerate(chunks):
        chunk["embedding"] = response.data[i].embedding
    return chunks

def index_to_vectorstore(chunks: list[dict]):
    VECTORSTORE_PATH.parent.mkdir(parents=True, exist_ok=True)
    VECTORSTORE_PATH.write_text(json.dumps(chunks, ensure_ascii=False), encoding="utf-8")
    
    # Save to FAISS index
    if chunks:
        embeddings = np.array([chunk["embedding"] for chunk in chunks], dtype="float32")
        dim = embeddings.shape[1]
        index = faiss.IndexFlatIP(dim) # Inner product for normalized embeddings
        index.add(embeddings)
        faiss.write_index(index, str(FAISS_INDEX_PATH))
        
    print(f"✓ Đã index {len(chunks)} chunks vào {VECTORSTORE_PATH.name} và FAISS ({FAISS_INDEX_PATH.name})")

def run_pipeline():
    docs = load_documents()
    chunks = chunk_documents(docs)
    chunks = embed_chunks(chunks)
    index_to_vectorstore(chunks)

if __name__ == "__main__":
    run_pipeline()
