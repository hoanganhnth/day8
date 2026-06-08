"""Retrieval layer for the group RAG pipeline.

Owner branch: `feature/retrieval-pipeline`.

Expected responsibilities:
- load standardized data selected by the group
- chunk/index documents
- run semantic search
- run lexical/BM25 search
- merge as hybrid retrieval
- apply retrieval fallback when needed
"""

from __future__ import annotations

from .utils import SourceDocument


import sys
import os

# Add the individual submission to sys.path to allow importing despite dashes in the folder name
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
individual_path = os.path.join(root_dir, "individual_submissions", "Day08-2A202600822-NguyenDuongHieu")
if individual_path not in sys.path:
    sys.path.append(individual_path)

try:
    from src.task5_semantic_search import semantic_search  # type: ignore
    from src.task6_lexical_search import lexical_search  # type: ignore
    from src.task7_reranking import reciprocal_rank_fusion  # type: ignore
    from src.task8_pageindex_vectorless import pageindex_search  # type: ignore
    IMPORTS_SUCCESS = True
except ImportError as e:
    print(f"[Warning] Group retrieval missing dependencies: {e}")
    IMPORTS_SUCCESS = False


SCORE_THRESHOLD = 0.45

def retrieve(
    question: str,
    top_k: int = 5,
    use_reranking: bool = True,
) -> list[SourceDocument]:
    """
    Return source documents relevant to the question.

    This integrated pipeline uses the individual submission for semantic,
    lexical, reranking, and fallback mechanisms.
    """
    if not IMPORTS_SUCCESS:
        return []

    print(f"\n[Group Retrieval] Đang xử lý: '{question}'")
    
    # 1. Semantic Search
    dense_results = semantic_search(question, top_k=top_k * 2)
    best_dense_score = dense_results[0]["score"] if dense_results else 0.0
    print(f"  -> Semantic Best Score: {best_dense_score:.3f}")
    
    # 2. Check Fallback
    if best_dense_score < SCORE_THRESHOLD:
        print(f"  ⚠ Score ({best_dense_score:.3f}) < Ngưỡng ({SCORE_THRESHOLD}). FALLBACK: PageIndex RAG!")
        fallback_results = pageindex_search(question, top_k=top_k)
        if fallback_results:
            for item in fallback_results:
                item["source"] = "pageindex"
            return fallback_results
        print("  -> PageIndex không có kết quả. Dùng Hybrid.")
        
    # 3. Lexical Search
    print("  -> Chạy Lexical Search (BM25)...")
    sparse_results = lexical_search(question, top_k=top_k * 2)
    
    # 4. Reranking & Fusion
    if use_reranking:
        print("  -> Trộn bằng RRF...")
        merged = reciprocal_rank_fusion(dense_results, sparse_results)
    else:
        merged = dense_results
        
    # 5. Build output conforming to SourceDocument
    final_docs = []
    for item in merged[:top_k]:
        final_docs.append(SourceDocument(
            content=item["content"],
            score=item["score"],
            source=item.get("source", "hybrid"),
            metadata=item.get("metadata", {})
        ))
        
    return final_docs
