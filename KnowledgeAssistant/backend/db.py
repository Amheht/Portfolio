# backend/db.py

import sqlite3
import json
import os
from typing import Dict, List, Optional

# Database file location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "knowledge.db")

# Get connection to SQLite database
def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row # Access rows like dicts.
    return conn

# Verifies 'users' table
def isvalid_users_table(cursor: sqlite3.Cursor) -> bool:
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        return True
    
    except Exception as e:
        print(f"users table creation failed: {e}")
        return False
    
# Verifies 'documents' table
def isvalid_documents_table(cursor: sqlite3.Cursor)  -> bool:
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER DEFAULT NULL,
                content TEXT NOT NULL,
                embedding TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)    
            )
        """)
        return True

    except Exception as e:
        print(f"'documents' table creation failed: {e}")
        return False

# Initializes the database
def init_db() -> bool:

    with sqlite3.connect(DATABASE_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        users_ok = isvalid_users_table(cursor)
        documents_ok = isvalid_documents_table(cursor)

        conn.commit()

    if not users_ok or not documents_ok:
        print("Database initialization failed. Check table creation logs.")
        return False
    return True


# Saves document to database
def save_document(content: str, embedding: List[float], user_id: Optional[int] = None) -> bool:
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO documents (user_id, content, embedding)
                VALUES (?, ?, ?)
            """, (user_id, content, json.dumps(embedding)))

            conn.commit()
        return True
    
    except Exception as e:
        print(f"Error saving document: {e}")
        return False

# Get all documents from database
def get_all_documents() -> List[Dict]:
    documents = []
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM documents")
            rows = cursor.fetchall()
        
            for row in rows:
                documents.append({
                    "id": row["id"],
                    "content": row["content"],
                    "embedding": json.loads(row["embedding"]),
                    "user_id": row["user_id"],
                    "created_at": row["created_at"]
                })

    except Exception as e:
        print(f"Failed to get all documents: {e}")

    return documents