# backend/openai_utils.py

import os
import openai
from dotenv import load_dotenv

# Load env variables from .env
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_embedding(text: str, model: str = "text-embedding-ada-002") -> list:
    """ Generates an embedding vector for a given text. """
    response = openai.Embedding.create(
        input=text,
        model=model
    )
    return response["data"][0]["embedding"]

def generate_answer(prompt: str, model = "gpt-4o") -> str:
    """ Generate a response based on a given prompt. """
    response = openai.ChatCompletition.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an internal knowledge assistant. Answer clearly and helpfully."},
            {"role": "user", "conent": prompt}
        ],
        temperature=0.2 # Range: 0.0 (Very deterministic; safe) to 1.0 (Creative; unexpected responses)
    )
    return response["choices"][0]["message"]["content"].strip()