import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.task5_semantic_search import semantic_search
from src.task6_lexical_search import lexical_search
from src.task7_reranking import rerank
from src.task8_pageindex_vectorless import pageindex_search

def retrieve(query: str, top_k: int = 5, score_threshold: float = 0.3) -> list[dict]:
    sem_res = semantic_search(query, top_k=top_k)
    lex_res = lexical_search(query, top_k=top_k)
    
    combined = sem_res + lex_res
    
    unique = {}
    for r in combined:
        if r["content"] not in unique:
            unique[r["content"]] = r
    candidates = list(unique.values())
    
    reranked = rerank(query, candidates, top_k=top_k)
    
    for r in reranked:
        r["source"] = "hybrid"
        
    if not reranked or reranked[0]["score"] < score_threshold:
        fallback = pageindex_search(query, top_k=top_k)
        return fallback
        
    return reranked[:top_k]
