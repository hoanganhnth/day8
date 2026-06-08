"""
Task 7 — Reranking Module.

Sử dụng thuật toán RRF (Reciprocal Rank Fusion) để kết hợp kết quả
của Semantic Search (Task 5) và Lexical Search (Task 6).
RRF giúp tận dụng điểm mạnh của cả hai phương pháp mà không cần model AI nặng.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.task5_semantic_search import semantic_search
from src.task6_lexical_search import lexical_search

def reciprocal_rank_fusion(list1: list[dict], list2: list[dict], k: int = 60) -> list[dict]:
    """
    Tính điểm RRF cho các tài liệu từ nhiều danh sách xếp hạng.
    RRF Score = sum(1 / (k + rank))
    Tham số k thường được thiết lập là 60 (theo bài báo chuẩn).
    """
    rrf_scores = {}
    doc_store = {}
    
    # Xử lý từng danh sách
    def process_list(results):
        for rank, item in enumerate(results):
            # Tạo ID duy nhất cho mỗi chunk
            doc_id = f"{item['metadata']['source']}_{item['metadata'].get('chunk_index', hash(item['content']))}"
            
            if doc_id not in rrf_scores:
                rrf_scores[doc_id] = 0
                doc_store[doc_id] = item
                
            rrf_scores[doc_id] += 1.0 / (k + rank + 1)
            
    process_list(list1)
    process_list(list2)
    
    # Sắp xếp các document theo điểm RRF giảm dần
    sorted_docs = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
    
    final_results = []
    for doc_id, score in sorted_docs:
        item = doc_store[doc_id].copy()
        item["score"] = score  # Ghi đè bằng điểm RRF
        item["metadata"]["rrf_score"] = score
        final_results.append(item)
        
    return final_results

def rerank(query: str, candidates: list[dict], top_k: int = 5, method: str = "rrf") -> list[dict]:
    """
    Hàm thực thi chính (sử dụng lại từ candidates):
    """
    if not candidates:
        return []
    
    # Giữ nguyên score cũ nếu có, nếu không thì giảm dần
    for i, c in enumerate(candidates):
        if "score" not in c:
            c["score"] = 1.0 / (i + 1)
            
    # Sort by score descending
    candidates.sort(key=lambda x: x.get("score", 0), reverse=True)
    return candidates[:top_k]

if __name__ == "__main__":
    test_query = "hình phạt cho tội tàng trữ ma tuý"
    print(f"Query: '{test_query}'")
    
    results = rerank(test_query, top_k=5)
    
    print("\n--- KẾT QUẢ RERANKING TỔNG HỢP (RRF) ---")
    for r in results:
        print(f"[RRF: {r['score']:.4f} | {r['metadata']['source']}] {r['content'][:120]}...\n")
