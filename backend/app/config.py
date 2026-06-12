import os


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/pokersense",
)

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
