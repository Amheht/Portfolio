# backend/db.py

from typing import List, Dict

# RAM storage (for testing)
documents = []

def save_document(content: str, embedding: List[float]) -> None:
    documents.append({
        "conent": content,
        "embedding": embedding
    })

def get_all_documents() -> List[Dict]:
    return documents