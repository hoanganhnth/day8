def rerank(query: str, candidates: list[dict], top_k: int = 5) -> list[dict]:
    if not candidates:
        return []
    
    reranked = []
    for c in candidates:
        score = c.get("score", 0.0)
        if query.lower() in c.get("content", "").lower():
            score += 0.5
        reranked.append({
            "content": c.get("content", ""),
            "score": score,
            "metadata": c.get("metadata", {})
        })
        
    reranked.sort(key=lambda x: x["score"], reverse=True)
    return reranked[:top_k]
