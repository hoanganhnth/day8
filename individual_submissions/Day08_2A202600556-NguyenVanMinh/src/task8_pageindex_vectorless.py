"""
Task 8 — PageIndex Vectorless RAG.

Đăng ký tài khoản tại: https://pageindex.ai/
SDK & sample code: https://github.com/VectifyAI/PageIndex

PageIndex cho phép RAG mà không cần vector store — sử dụng
structural understanding của document thay vì embedding.

Cài đặt:
    pip install pageindex

Hướng dẫn:
    1. Đăng ký account tại pageindex.ai
    2. Lấy API key
    3. Upload documents
    4. Query sử dụng PageIndex API
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PAGEINDEX_API_KEY = os.getenv("PAGEINDEX_API_KEY", "")
STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"
LANDING_DIR = Path(__file__).parent.parent / "data" / "landing"


def upload_documents():
    """
    Upload toàn bộ markdown documents lên PageIndex.
    """
    from pageindex import PageIndexClient
    import time

    pi = PageIndexClient(api_key=PAGEINDEX_API_KEY)

    for pdf_file in LANDING_DIR.rglob("*.pdf"):
        try:
            # SDK hiện tại của PageIndex chỉ hỗ trợ PDF
            pi.submit_document(file_path=str(pdf_file))
            print(f"  [OK] Uploaded: {pdf_file.name}")
            time.sleep(1) # Tránh rate limit
        except Exception as e:
            print(f"  [Loi] upload {pdf_file.name}: {e}")


def pageindex_search(query: str, top_k: int = 5) -> list[dict]:
    """
    Vectorless retrieval sử dụng PageIndex.
    Dùng làm fallback khi hybrid search không có kết quả tốt.

    Args:
        query: Câu truy vấn
        top_k: Số lượng kết quả tối đa

    Returns:
        List of {
            'content': str,
            'score': float,
            'metadata': dict,
            'source': 'pageindex'   # Đánh dấu nguồn retrieval
        }
    """
    from pageindex import PageIndexClient
    import time

    pi = PageIndexClient(api_key=PAGEINDEX_API_KEY)
    
    # Lấy danh sách doc_ids đã upload
    try:
        docs = pi.list_documents(limit=10).get("documents", [])
    except Exception as e:
        print(f"[Loi] lay danh sach document: {e}")
        return []

    all_results = []
    
    # Tìm kiếm trên từng document (do SDK hiện tại submit_query yêu cầu doc_id)
    for doc in docs:
        doc_id = doc.get("id")
        if not doc_id:
            continue
            
        try:
            res = pi.submit_query(doc_id=doc_id, query=query)
            retrieval_id = res.get("retrieval_id")
            
            if retrieval_id:
                # Đợi kết quả trả về
                for _ in range(5):
                    time.sleep(1)
                    status_res = pi.get_retrieval(retrieval_id)
                    if status_res.get("status") == "completed":
                        # Trích xuất chunks từ kết quả (tuỳ theo format response của API)
                        chunks = status_res.get("results", [])
                        for chunk in chunks:
                            all_results.append({
                                "content": chunk.get("text", str(chunk)),
                                "score": chunk.get("score", 0.0),
                                "metadata": doc.get("name", ""),
                                "source": "pageindex"
                            })
                        break
        except Exception as e:
            print(f"[Loi] search doc {doc_id}: {e}")

    # Sort & return top_k
    all_results = sorted(all_results, key=lambda x: x["score"], reverse=True)
    return all_results[:top_k]


if __name__ == "__main__":
    import sys
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
        
    if not PAGEINDEX_API_KEY:
        print("⚠ Hãy set PAGEINDEX_API_KEY trong file .env")
        print("  Đăng ký tại: https://pageindex.ai/")
    else:
        print("Uploading documents...")
        upload_documents()

        print("\nTest query:")
        results = pageindex_search("hình phạt sử dụng ma tuý", top_k=3)
        for r in results:
            print(f"[{r['score']:.3f}] {r['content'][:100]}...")
