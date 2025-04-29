# backend/models.py

from pydantic import BaseModel, Field
from typing import List

class UploadDocumentRequest(BaseModel):
    content: str

class RegisterRequest(BaseModel):
    username: str = Field(..., example="bob")
    password: str = Field(..., example="apples")

class AskQuestionRequest(BaseModel):
    question: str