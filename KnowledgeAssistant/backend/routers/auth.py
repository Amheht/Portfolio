# backend/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from backend.db import get_connection
from backend.models import RegisterRequest, LoginRequest
from backend.auth_utils import hash_password, create_access_token, verify_password
from typing import Optional
import sqlite3

auth_router = APIRouter(prefix="/auth", tags=["auth"])

# === Internal login helper ===
def authenicate_user(username: str, password: str) -> Optional[str]:
    try:
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            
            if not user:
                return None

            hashed_password = user["hashed_password"]

            if not verify_password(password, hashed_password):
                return None
            
            # return authenticated username
            return username
    
    except Exception as e:
        return None

# === JSON Login ===   
@auth_router.post("/login")
async def login(request: LoginRequest):
    username = request.username.strip()
    password = request.password

    user = authenicate_user(username, password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password.")
    
    token = create_access_token({"sub": user})
    return {"access_token": token, "token_type": "bearer"}

# === Form Login ===
@auth_router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    user = authenicate_user(username, password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password.")
    
    token = create_access_token({"sub": user})
    return {"access_token": token, "token_type": "bearer"}

# === Regiser User Endpoint ===
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

