# backend/app.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.openai_utils import get_embedding
from backend.db import save_document


# Create FastAPI app
app = FastAPI(
    title="Knowledge Assistant API",
    description="An internal knowledge assistant powered by OpenAI",
    version="0.1.0"
)


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Root endpoint
@app.get("/")
async def root():
     return {"message": "Welcome to the Knowledge Assistant API!"}


# Upload Document Endpoint
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
