# Knowledge Assistant API

A lightweight internal knowledge assistant powered by OpenAI and FastAPI.


## Features


- User registration and login system (bcrypt + JWT)
- Secure token-based authentication
- Upload internal documents for knowledge storage
- Ask questions against uploaded documents (semantic search)
- Document embeddings powered by OpenAI
- Modular, production-grade backend structure
- Swagger UI documentation at '/docs/


## Technologies Used


- **Python 3.12**
- **FastAPI** (backend API framework)
- **SQLite** (lightweight database for storage)
- **bcrypt** (password hashing)
- **JWT** (token authentication)
- **OpenAI API** (embeddings and answer generation)


## Security Note

- Secret keys and sensitive credentials must be stored in a proper .env file.
- Always replace default SECRET_KEY before deploying publicly.

## Licence
This product is only for educational purposes.

## Author
Joseph Garcia

## Getting Started

### Requirements
- Python 3.10+
- Virtual environment recommended

```bash
# Clone the repository
git clone http://github.com/Amheht/Portfolio.git
cd Portfolio/KnowledgeAssistant

# Create virtual environment
python -m venv knowledge-assistant-venv

# Activate virtual environment (Windods)
knowledge-assistant-venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Running the server
uvicorn backend.app:app --reload