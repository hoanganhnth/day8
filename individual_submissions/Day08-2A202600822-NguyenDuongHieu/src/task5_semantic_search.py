"""
Task 5 — Semantic Search Module.

Viết module tìm kiếm ngữ nghĩa (dense retrieval) trên vector store.

Yêu cầu:
    - Input: query string + top_k
    - Output: danh sách chunks có score, sorted descending
    - Phải tương thích với embedding model và vector store ở Task 4
"""


import os
from pathlib import Path
import chromadb
import numpy as np

# Cấu hình phải khớp với Task 4
STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"
DB_PATH = str(Path(__file__).parent.parent.parent / "Day08_2A202600556-NguyenVanMinh" / "data" / "vectorstore" / "chroma_db")
EMBEDDING_MODEL = "BAAI/bge-m3"

class SemanticSearcher:
    def __init__(self):
        # KHỞI TẠO CHROMADB TRƯỚC! PyTorch (trong SentenceTransformer) làm hỏng ThreadPool của Rust trên Windows
        self.client = chromadb.PersistentClient(path=DB_PATH)
        self.collection = self.client.get_collection(name="DrugLawDocs")
        
        # Fix lỗi HNSW của Chroma trên Windows: tách làm 2 lần lấy để tránh bug
        data_text = self.collection.get(include=["documents", "metadatas"])
        data_emb = self.collection.get(ids=data_text["ids"], include=["embeddings"])
        
        self.documents = data_text["documents"]
        self.metadatas = data_text["metadatas"]
        self.embeddings = np.array(data_emb["embeddings"])
        
        # SAU ĐÓ MỚI LOAD MODEL
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        
        # Chuẩn hóa vector trước để tính toán siêu nhanh
        norms = np.linalg.norm(self.embeddings, axis=1, keepdims=True)
        self.embeddings_normalized = self.embeddings / norms

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        """
        Tìm kiếm ngữ nghĩa:
        1. Encode câu truy vấn thành vector
        2. Tính Cosine Similarity bằng Numpy
        3. Sắp xếp và trả về top_k kết quả
        """
        # Encode query
        query_embedding = self.model.encode(query).reshape(1, -1)
        query_norm = np.linalg.norm(query_embedding, axis=1, keepdims=True)
        query_normalized = query_embedding / query_norm
        
        # Dot product giữa các vector đã chuẩn hóa = Cosine Similarity
        similarities = np.dot(self.embeddings_normalized, query_normalized.T).flatten()
        
        # Lấy top K indices
        top_indices = similarities.argsort()[::-1][:top_k]
        
        output = []
        for idx in top_indices:
            output.append({
                "content": self.documents[idx],
                "score": float(similarities[idx]),
                "metadata": self.metadatas[idx]
            })
            
        return output

# Lazy load instance
_searcher_instance = None

def get_searcher():
    global _searcher_instance
    if _searcher_instance is None:
        _searcher_instance = SemanticSearcher()
    return _searcher_instance

# Hàm wrapper giữ nguyên signature ban đầu của bài tập
def semantic_search(query: str, top_k: int = 10) -> list[dict]:
    searcher = get_searcher()
    return searcher.search(query, top_k)

if __name__ == "__main__":
    print(f"Loading embedding model: {EMBEDDING_MODEL}...")
    results = semantic_search("hình phạt cho tội tàng trữ ma tuý", top_k=5)
    print("--- KẾT QUẢ TÌM KIẾM ---")
    for r in results:
        print(f"[{r['score']:.3f} | {r['metadata']['source']}] {r['content'][:100]}...")
