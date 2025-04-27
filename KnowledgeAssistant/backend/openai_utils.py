# backend/openai_utils.py

import os
from openai import OpenAI
from dotenv import load_dotenv

# Set the proper location for .env
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

# Load env variables from .env
load_dotenv(dotenv_path=dotenv_path)

# Set OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embedding(text: str, model: str = "text-embedding-ada-002") -> list:
    """ Generates an embedding vector for a given text. """
    response = client.embeddings.create(
        input=[text],
        model=model
    )
    return response.data[0].embedding

def generate_answer(prompt: str, model = "gpt-4o") -> str:
    """ Generate a response based on a given prompt. """
    if not prompt or not isinstance(prompt, str):
        raise ValueError("Prompt must be non empty string.")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system", 
                "content": "You are an internal knowledge assistant. Answer clearly and helpfully."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ],
        temperature=0.2 # Range: 0.0 (Very deterministic; safe) to 1.0 (Creative; unexpected responses)
    )
    return response.choices[0].message.content.strip()