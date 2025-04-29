# backend/auth_utils.py

from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
import os
import bcrypt

# Load secret key
SECRET_KEY = os.getenv("SECRET_KEY", "the_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Returns current time (timezone appropriate)
def now(utc: bool = True) -> datetime:
    return datetime.now(timezone.utc) if utc else datetime.now()

# Password hashing
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

# Password verification
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

# JWT token creation
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Verify jwt token
def decode_access_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None