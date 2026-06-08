"""
Task 5 — Semantic Search Module.

Viết module tìm kiếm ngữ nghĩa (dense retrieval) trên vector store.

Yêu cầu:
    - Input: query string + top_k
    - Output: danh sách chunks có score, sorted descending
    - Phải tương thích với embedding model và vector store ở Task 4
"""


def semantic_search(query: str, top_k: int = 10) -> list[dict]:
    """
    Tìm kiếm ngữ nghĩa sử dụng vector similarity.

    Args:
        query: Câu truy vấn
        top_k: Số lượng kết quả tối đa

    Returns:
        List of {
            'content': str,      # Nội dung chunk
            'score': float,      # Cosine similarity score
            'metadata': dict     # source, doc_type, chunk_index
        }
        Sorted by score descending.
    """
    from sentence_transformers import SentenceTransformer
    import chromadb
    from pathlib import Path

    # 1. Khởi tạo kết nối tới ChromaDB giống y như Task 4
    db_path = str(Path(__file__).parent.parent / "data" / "vectorstore" / "chroma_db")
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_collection(name="DrugLawDocs")

    # 2. Embed câu truy vấn bằng mô hình BAAI/bge-m3
    model = SentenceTransformer("BAAI/bge-m3")
    query_embedding = model.encode(query).tolist()

    # 3. Tìm kiếm trong ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    # 4. Format lại kết quả trả về
    formatted_results = []
    if results and results["documents"] and len(results["documents"]) > 0:
        docs = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]
        
        for doc, meta, dist in zip(docs, metadatas, distances):
            # ChromaDB trả về distance (khoảng cách), ta quy đổi sang similarity score (điểm tương đồng)
            # Vì ở Task 4 dùng cosine, score = 1 - distance
            score = 1.0 - dist
            formatted_results.append({
                "content": doc,
                "score": float(score),
                "metadata": meta
            })
            
    return formatted_results


if __name__ == "__main__":
    # Test
    results = semantic_search("hình phạt cho tội tàng trữ ma tuý", top_k=5)
    for r in results:
        print(f"[{r['score']:.3f}] {r['content'][:100]}...")
