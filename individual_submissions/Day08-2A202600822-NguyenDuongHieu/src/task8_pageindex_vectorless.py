import os
import json
import time
from pathlib import Path
from pageindex import PageIndexClient

DOC_IDS_FILE = Path(__file__).parent / "pageindex_docs.json"

def get_pageindex_client():
    api_key = os.getenv("PAGEINDEX_API_KEY")
    if not api_key:
        print("[CHÚ Ý] Bạn cần có PAGEINDEX_API_KEY để chạy Vectorless RAG.")
        print("Vui lòng đăng ký tài khoản miễn phí tại: https://pageindex.ai/")
        print("Và thiết lập biến môi trường PAGEINDEX_API_KEY.")
        return None
    return PageIndexClient(api_key=api_key)

def setup_pageindex_documents():
    """
    Lấy danh sách các tài liệu đã có trên PageIndex.
    Nếu chưa có, sẽ tiến hành upload (bỏ qua các file vượt quá giới hạn Free Tier).
    """
    client = get_pageindex_client()
    
    # 1. Thử lấy danh sách tài liệu từ API luôn (an toàn hơn lưu file cục bộ)
    try:
        existing_docs = client.list_documents().get("documents", [])
        if existing_docs:
            doc_ids = [doc["id"] for doc in existing_docs]
            print(f"Đã load {len(doc_ids)} tài liệu từ tài khoản PageIndex của bạn.")
            return client, doc_ids
    except Exception as e:
        print(f"Lỗi khi check danh sách tài liệu: {e}")
            
    # 2. Nếu chưa có gì, bắt đầu upload
    doc_ids = []
    pdf_dir = Path(__file__).parent.parent / "data" / "landing" / "legal"
    
    print("\nBắt đầu upload tài liệu lên PageIndex...")
    for pdf_file in pdf_dir.glob("*.pdf"):
        print(f"Đang upload: {pdf_file.name} ...")
        try:
            res = client.submit_document(str(pdf_file))
            doc_id = res["doc_id"]
            doc_ids.append(doc_id)
            print(f" -> Thành công! Document ID: {doc_id}")
        except Exception as e:
            print(f" -> [Bỏ qua] Upload thất bại (Có thể do file quá lớn vượt mức Free Tier): {e}")
        
    print("\n[LƯU Ý QUAN TRỌNG]")
    print("Hệ thống sẽ mất từ 1-3 phút để phân tích OCR và xây dựng Tree structure.")
    print("Lần đầu chạy có thể bị báo 'chưa sẵn sàng', bạn chỉ cần chờ một lát rồi chạy lại nhé!")
    
    return client, doc_ids

def pageindex_search(query: str, top_k: int = 5) -> list[dict]:
    """
    Vectorless retrieval using PageIndex.
    Fallback khi hybrid search không trả về kết quả phù hợp.
    """
    client, doc_ids = setup_pageindex_documents()
    if not client:
        return []
    
    results = []
    print(f"\nĐang truy vấn bằng Vectorless RAG với câu hỏi: '{query}'")
    
    for doc_id in doc_ids:
        try:
            # 1. Kiểm tra tài liệu đã xử lý xong chưa
            if not client.is_retrieval_ready(doc_id):
                print(f"[Warning] Tài liệu {doc_id} chưa sẵn sàng. Bỏ qua.")
                continue
                
            # 2. Gửi câu truy vấn
            res = client.submit_query(doc_id, query)
            retrieval_id = res["retrieval_id"]
            
            # 3. Chờ kết quả trả về
            while True:
                ret = client.get_retrieval(retrieval_id)
                status = ret.get("status")
                
                if status == "completed":
                    # Trích xuất các nội dung tìm được
                    nodes = ret.get("retrieved_nodes", [])
                    for node in nodes:
                        content_str = ""
                        # PageIndex trả về structure relevant_contents là list of list of dicts
                        for block in node.get("relevant_contents", []):
                            for subblock in block:
                                content_str += subblock.get("relevant_content", "") + "\n\n"
                        
                        score = node.get("score", 0.5)
                        results.append({
                            "content": content_str.strip(),
                            "score": score,
                            "metadata": {"source": f"pageindex_doc"}
                        })
                    break
                elif status == "failed":
                    print(f"[Error] Truy vấn thất bại cho doc {doc_id}")
                    break
                
                # Chờ 2 giây rồi hỏi lại server
                time.sleep(2)
                
        except Exception as e:
            print(f"[Error] Lỗi khi truy vấn: {e}")
            
    # 4. Sắp xếp theo điểm số và lấy top_k
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    return results[:top_k]

if __name__ == "__main__":
    # Đổi câu hỏi test cho phù hợp với Luật Phòng chống ma túy 2021 (tài liệu đã được up lên)
    test_query = "các biện pháp cai nghiện ma túy"
    
    # Do pageindex trả về list node, ta sẽ test thử:
    res = pageindex_search(test_query, top_k=5)
    
    if res:
        print("\n--- KẾT QUẢ TỪ PAGEINDEX (VECTORLESS RAG) ---")
        for i, r in enumerate(res):
            print(f"{i+1}. [Score: {r['score']}] {r['content'][:150]}...\n")
    else:
        print("\nKhông tìm thấy kết quả hoặc tài liệu đang trong quá trình xử lý.")
