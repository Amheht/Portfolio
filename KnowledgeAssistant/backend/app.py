# backend/app.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from backend.openai_utils import get_embedding, generate_answer
from backend.db import save_document, get_all_documents


# === Create FastAPI app ===
app = FastAPI(
    title="Knowledge Assistant API",
    description="An internal knowledge assistant powered by OpenAI",
    version="0.1.0"
)


# === Health Check Endpoint ===
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# === Root Endpoint ===
@app.get("/")
async def root():
     return {"message": "Welcome to the Knowledge Assistant API!"}


# === Upload Document Endpoint ===
class UploadDocumentRequest(BaseModel):
    content: str


@app.post("/upload")
async def upload_document(request: UploadDocumentRequest):
    try:
        # Get text from request.
        content = request.content

        # Create embedding from content.
        embedding = get_embedding(content)

        # Save document and embedding to storage.
        save_document(content, embedding) 

        # Return success.
        return {"message": "Document upload successfully!"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload document: {str(e)}")


# === Add Question Endpoint ===
class AskQuestionRequest(BaseModel):
    question: str

@app.post("/ask-question")
async def ask_question(request: AskQuestionRequest):
    try:
        question = request.question

        question_embedding = get_embedding(question)

        documents = get_all_documents()

        if not documents:
            raise HTTPException(status_code=404, detail="No reference documents found for answering questions.")
        
        best_doc = find_most_similar_document(question_embedding, documents)

        prompt = f"Use the following document to answer the question. \n\nDocument:\n{best_doc['content']}\n\nQuestion:\n{question}"

        answer = generate_answer(prompt)

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
def find_most_similar_document(question_embedding: List[float], documents: List[dict]) -> dict:
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
            best_doct = doc

    return best_doc