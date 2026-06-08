"""
Task 9 — Retrieval Pipeline Hoàn Chỉnh.

Kết hợp semantic search + lexical search + reranking + PageIndex fallback
thành một pipeline thống nhất.

Logic:
    1. Chạy semantic_search + lexical_search song song
    2. Merge kết quả (RRF hoặc weighted fusion)
    3. Rerank
    4. Nếu top result score < threshold → fallback sang PageIndex
    5. Return top_k results
"""

import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.task5_semantic_search import semantic_search
from src.task6_lexical_search import lexical_search
from src.task7_reranking import reciprocal_rank_fusion
from src.task8_pageindex_vectorless import pageindex_search


# =============================================================================
# CONFIGURATION
# =============================================================================

SCORE_THRESHOLD = 0.45   # Ngưỡng cosine similarity tối thiểu
DEFAULT_TOP_K = 5

def retrieve(
    query: str,
    top_k: int = DEFAULT_TOP_K,
    score_threshold: float = SCORE_THRESHOLD,
    use_reranking: bool = True,
) -> list[dict]:
    print("\n" + "="*50)
    print(f"[PIPELINE] Bắt đầu xử lý truy vấn: '{query}'")
    
    # Step 1: Chạy Semantic Search để kiểm tra độ phù hợp
    dense_results = semantic_search(query, top_k=top_k * 2)
    best_dense_score = dense_results[0]["score"] if dense_results else 0.0
    print(f"  -> Semantic Best Score: {best_dense_score:.3f}")
    
    # Step 2: Nếu điểm Semantic quá thấp (nhỏ hơn threshold), Fallback sang PageIndex
    if best_dense_score < score_threshold:
        print(f"  ⚠ Điểm Semantic ({best_dense_score:.3f}) < Ngưỡng ({score_threshold}).")
        print("  -> Kích hoạt FALLBACK: Vectorless RAG (PageIndex)!")
        
        fallback_results = pageindex_search(query, top_k=top_k)
        
        if fallback_results:
            for item in fallback_results:
                item["source"] = "pageindex"
            return fallback_results
        else:
            print("  -> PageIndex không tìm thấy kết quả phù hợp. Trả về kết quả Hybrid hiện có.")
    
    # Step 3: Nếu điểm cao hoặc Fallback thất bại, chạy tiếp Lexical và Merge
    print("  -> Chạy Lexical Search (BM25)...")
    sparse_results = lexical_search(query, top_k=top_k * 2)
    
    if use_reranking:
        print("  -> Trộn và xếp hạng lại bằng RRF...")
        merged = reciprocal_rank_fusion(dense_results, sparse_results)
    else:
        merged = dense_results
        
    for item in merged:
        item["source"] = "hybrid"
        
    return merged[:top_k]


if __name__ == "__main__":
    test_queries = [
        "Hình phạt cho tội tàng trữ trái phép chất ma tuý",
        "Nghệ sĩ nào bị bắt vì sử dụng ma tuý năm 2024",
        "Luật phòng chống ma tuý 2021 quy định gì về cai nghiện",
    ]

    for q in test_queries:
        print(f"\nQuery: {q}")
        print("-" * 60)
        results = retrieve(q, top_k=3)
        for i, r in enumerate(results, 1):
            print(f"  {i}. [{r['score']:.3f}] [{r['source']}] {r['content'][:80]}...")
