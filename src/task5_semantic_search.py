import json
import os
import math
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import faiss
import numpy as np

load_dotenv()

VECTORSTORE_PATH = Path(__file__).parent.parent / "data" / "vectorstore.json"
FAISS_INDEX_PATH = Path(__file__).parent.parent / "data" / "vectorstore.index"
EMBEDDING_MODEL = "text-embedding-3-small"

def semantic_search(query: str, top_k: int = 10) -> list[dict]:
    if not VECTORSTORE_PATH.exists() or not FAISS_INDEX_PATH.exists():
        return []
    
    chunks = json.loads(VECTORSTORE_PATH.read_text(encoding="utf-8"))
    
    client = OpenAI()
    response = client.embeddings.create(input=[query], model=EMBEDDING_MODEL)
    query_emb = np.array([response.data[0].embedding], dtype="float32")
    
    index = faiss.read_index(str(FAISS_INDEX_PATH))
    scores, indices = index.search(query_emb, top_k)
    
    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx != -1 and idx < len(chunks):
            chunk = chunks[idx]
            results.append({
                "content": chunk["content"],
                "score": float(score),
                "metadata": chunk.get("metadata", {})
            })
            
    return results
