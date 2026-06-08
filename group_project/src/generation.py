"""Generation and citation formatting for the group RAG pipeline.

Owner branch: `feature/generation-citation`.
"""

from __future__ import annotations
import os
import sys

from .utils import NOT_INTEGRATED_MESSAGE, SourceDocument

# Add the individual submission to sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
individual_path = os.path.join(root_dir, "individual_submissions", "Day08-2A202600821-LeNguyenMinhQuan")
if individual_path not in sys.path:
    sys.path.append(individual_path)

try:
    from src.task10_generation import generate_with_citation as llm_generate  # type: ignore
    IMPORTS_SUCCESS = True
except ImportError as e:
    print(f"[Warning] Group generation missing dependencies: {e}")
    IMPORTS_SUCCESS = False

def generate_with_citation(question: str, sources: list[SourceDocument]) -> str:
    """
    Generate a cited answer from retrieved source documents.
    """
    if not IMPORTS_SUCCESS:
        return NOT_INTEGRATED_MESSAGE
        
    if not sources:
        return NOT_INTEGRATED_MESSAGE

    # Convert SourceDocument to dict for task10_generation
    context_chunks = []
    for s in sources:
        context_chunks.append({
            "content": s.get("content", ""),
            "metadata": s.get("metadata", {}),
            "source": s.get("source", "hybrid")
        })

    # Call the actual generation logic
    result = llm_generate(question, context_chunks)
    return result["answer"]
