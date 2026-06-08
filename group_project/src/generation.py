"""Generation and citation formatting for the group RAG pipeline.

Owner branch: `feature/generation-citation`.
"""

from __future__ import annotations
import sys
from pathlib import Path

from .utils import NOT_INTEGRATED_MESSAGE, SourceDocument

# Tích hợp hàm generate_with_citation từ bài cá nhân của LeNguyenMinhQuan
base_dir = Path(__file__).parent.parent.parent
indiv_src_dir = base_dir / "individual_submissions" / "Day08-2A202600821-LeNguyenMinhQuan" / "src"
if str(indiv_src_dir) not in sys.path:
    sys.path.append(str(indiv_src_dir))

try:
    from task10_generation import generate_with_citation as t10_generate
except ImportError:
    t10_generate = None


def generate_with_citation(question: str, sources: list[SourceDocument]) -> str:
    """
    Generate a cited answer from retrieved source documents.
    """
    if not sources:
        return "Xin lỗi, tôi không tìm thấy thông tin nào liên quan đến câu hỏi của bạn trong cơ sở dữ liệu."
        
    if t10_generate is None:
        return NOT_INTEGRATED_MESSAGE

    # Chuyển đổi định dạng SourceDocument của nhóm sang dict format của Task 10
    context_chunks = []
    for s in sources:
        context_chunks.append({
            "content": s.get("content", ""),
            "metadata": s.get("metadata", {})
        })
        
    # Gọi hàm xịn sò đã gắn OpenAI từ bài cá nhân
    result = t10_generate(question, context_chunks)
    return result.get("answer", NOT_INTEGRATED_MESSAGE)
