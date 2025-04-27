# backend/models.py

from pydantic import BaseModel
from typing import List

class UploadDocumentRequest(BaseModel):
    content: str