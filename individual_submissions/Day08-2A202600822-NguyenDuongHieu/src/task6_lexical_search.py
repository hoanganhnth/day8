import os
from pathlib import Path
from rank_bm25 import BM25Okapi
import chromadb
import string

STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"
DB_PATH = "D:/code/chroma_db_cohort2"

class LexicalSearcher:
    def __init__(self):
        print("Loading all documents from ChromaDB for BM25...")
        # Lấy toàn bộ chunk từ database đã làm ở Task 4
        self.client = chromadb.PersistentClient(path=DB_PATH)
        self.collection = self.client.get_collection(name="drug_law_docs")
        
        # Get tất cả dữ liệu
        all_data = self.collection.get(include=["documents", "metadatas"])
        
        self.documents = all_data["documents"]
        self.metadatas = all_data["metadatas"]
        
        # Tokenize corpus: Loại bỏ dấu câu cơ bản và tách từ (whitespace)
        tokenized_corpus = [self._tokenize(doc) for doc in self.documents]
        
        print("Building BM25 Index...")
        self.bm25 = BM25Okapi(tokenized_corpus)

    def _tokenize(self, text: str) -> list[str]:
        # Hàm tokenize đơn giản: lower case, xóa dấu câu cơ bản
        text = text.lower()
        for p in string.punctuation:
            text = text.replace(p, ' ')
        return text.split()

    def search(self, query: str, top_k: int = 10) -> list[dict]:
        tokenized_query = self._tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)
        
        # Tạo danh sách kết quả kèm score
        results = []
        for i, score in enumerate(scores):
            if score > 0:  # Chỉ lấy những văn bản có điểm > 0 (có khớp từ)
                results.append({
                    "content": self.documents[i],
                    "score": float(score),
                    "metadata": self.metadatas[i]
                })
        
        # Sắp xếp giảm dần theo điểm BM25
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

# Lazy load
_lexical_searcher = None

def lexical_search(query: str, top_k: int = 10) -> list[dict]:
    """
    Tìm kiếm từ khóa (Lexical Search) sử dụng thuật toán BM25.

    Args:
        query: Câu truy vấn
        top_k: Số lượng kết quả tối đa

    Returns:
        List of {'content': str, 'score': float, 'metadata': dict}
    """
    global _lexical_searcher
    if _lexical_searcher is None:
        _lexical_searcher = LexicalSearcher()
    return _lexical_searcher.search(query, top_k)

if __name__ == "__main__":
    results = lexical_search("hình phạt cho tội tàng trữ ma tuý", top_k=5)
    print("--- KẾT QUẢ TÌM KIẾM TỪ KHÓA (BM25) ---")
    for r in results:
        print(f"[Score: {r['score']:.2f} | {r['metadata']['source']}] {r['content'][:100]}...")
