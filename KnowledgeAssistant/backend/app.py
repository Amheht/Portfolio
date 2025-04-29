# backend/app.py


from fastapi import FastAPI
from backend.db import init_db
from backend.routers.auth import auth_router
from backend.routers.knowledge import knowledge_router

# Create FastAPI app
app = FastAPI(
    title="Knowledge Assistant API",
    description="An internal knowledge assistant powered by OpenAI",
    version="0.1.0"
)

# Initialize Database
if not init_db():
    raise Exception("Database initialization failed. Cannot start server.")

# Routers
app.include_router(auth_router)
app.include_router(knowledge_router)

# === Root Endpoint ===
@app.get("/")
async def root():
     return {"message": "Welcome to the Knowledge Assistant API!"}

# === Health Check Endpoint ===
@app.get("/health")
async def health_check():
    return {"status": "ok"}