# backend/app.py

from fastapi import FastAPI

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