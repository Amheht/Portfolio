# backend/routers/auth.py

from fastapi import APIRouter, HTTPException
from backend.db import get_connection
from backend.models import RegisterRequest
from backend.auth_utils import hash_password
import sqlite3

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/register")
async def register_user(request: RegisterRequest):
    try:
        username = request.username.strip()
        password = request.password

        if not username or not password:
            raise HTTPException(status_code=400, detail="Username and password cannot be empty.")

        hashed_password = hash_password(password)

        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                raise HTTPException(status_code=400, detail="Username already exists in database.")
            
            cursor.execute(
                "INSERT INTO users (username, hashed_password) VALUES (?, ?)",
                (username, hashed_password)
            )
            conn.commit()
        
        return {"message": "User successfully registered!"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")
