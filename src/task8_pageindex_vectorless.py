def pageindex_search(query: str, top_k: int = 5) -> list[dict]:
    results = []
    for i in range(top_k):
        results.append({
            "content": f"PageIndex result {i} for {query}",
            "score": 0.8 - i * 0.1,
            "source": "pageindex",
            "metadata": {"source": "pageindex_mock"}
        })
    return results
