# backend/routers/knowledge.py

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional, Tuple

from backend.db import get_all_documents, save_document
from backend.models import AskQuestionRequest, UploadDocumentRequest
from backend.auth_utils import get_current_user
from backend.openai_utils import get_embedding, generate_answer

knowledge_router = APIRouter(prefix="/knowledge", tags=["knowledge"])

CONFIDENCE_THRESHOLD = 0.7
MINIMUM_CONTENT_LENGTH = 20

# === Upload Document Endpoint ===
@knowledge_router.post("/upload")
async def upload_document(request: UploadDocumentRequest, username: str = Depends(get_current_user)):
    try:
        # Get text from request.
        content = request.content

        # Create embedding from content.
        embedding = get_embedding(content)

        # TODO: Attach username to document uploads.

        # Save document and embedding to storage.
        save_document(content, embedding) 

        # Return success.
        return {"message": "Document upload successfully!"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload document: {str(e)}")


# === Add Question Endpoint ===
@knowledge_router.post("/ask-question")
async def ask_question(request: AskQuestionRequest, username: str = Depends(get_current_user)):
    try:
        question = request.question

        # Create embedding for question
        question_embedding = get_embedding(question)

        # TODO: filter docs by username and access.
        # Get the documents from the database
        documents = get_all_documents()
        if not documents:
            return {"answer": "No documents are currently available in the knowledge base."}
        
        # Find the most similar document
        best_doc, best_score = find_most_similar_document(question_embedding, documents)
        if best_doc is None or best_score < CONFIDENCE_THRESHOLD:
            return {"answer": "It doesn't appear that I can find a suitable document to answer your question."}
        
        # Validate document content
        if not best_doc.get('content') or len(best_doc['content'].strip()) < MINIMUM_CONTENT_LENGTH:
            return {"answer": "It doesn't appear that I can find a suitable document to answer your question."}

        # Create the prompt and generate answer
        prompt = f"Use the following document to answer the question. \n\nDocument:\n{best_doc['content']}\n\nQuestion:\n{question}"
        answer = generate_answer(prompt)

        # Response with answer
        return {"answer": answer}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to answer question: {str(e)}")


# === Helper Function: Cosine Similarity ===
def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    """ 
    Compute cosine similarity between two vectors. 
    
    Args:
        vec1: list of floats.
        vec2: list of floats.
    
    Return: the similarity between vec1 and vec2
    """

    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = sum(a * a for a in vec1) ** 0.5
    norm2 = sum(b * b for b in vec2) ** 0.5
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return dot_product / (norm1 * norm2)

# === Helper Function: Find Most Similar Document ===
def find_most_similar_document(question_embedding: List[float], documents: List[dict]) -> Tuple[Optional[dict], float]:
    """ 
    Find the document with the highest similarity to the question
    
    Args:
        question_embedding: the question
        documents: the documents to search.

    Return: The document most similar to the question.
    """

    best_score = -1
    best_doc = None
    for doc in documents:
        score = cosine_similarity(question_embedding, doc["embedding"])
        if score > best_score:
            best_score = score
            best_doc = doc

    return best_doc, best_score