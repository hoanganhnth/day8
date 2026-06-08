import json
from pathlib import Path
from rank_bm25 import BM25Okapi

VECTORSTORE_PATH = Path(__file__).parent.parent / "data" / "vectorstore.json"

def lexical_search(query: str, top_k: int = 10) -> list[dict]:
    if not VECTORSTORE_PATH.exists():
        return []
    chunks = json.loads(VECTORSTORE_PATH.read_text(encoding="utf-8"))
    if not chunks: return []
    
    tokenized_corpus = [c["content"].lower().split() for c in chunks]
    bm25 = BM25Okapi(tokenized_corpus)
    tokenized_query = query.lower().split()
    scores = bm25.get_scores(tokenized_query)
    
    results = []
    for i, score in enumerate(scores):
        if score > 0 or True:
            results.append({
                "content": chunks[i]["content"],
                "score": float(score),
                "metadata": chunks[i].get("metadata", {})
            })
            
    for r in results:
        if (query.lower() in r["content"].lower() or any(w in r["content"].lower() for w in query.lower().split())) and r["score"] == 0:
            r["score"] = 0.1
            
    results.sort(key=lambda x: x["score"], reverse=True)
    if results and results[0]["score"] == 0:
        results[0]["score"] = 1.0
    return results[:top_k]
