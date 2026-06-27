import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini")

    EMBEDDING_MODEL: str = os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    VECTOR_DB_DIR: str = os.getenv("VECTOR_DB_DIR", "vector_store")
    DATA_DIR: str = os.getenv("DATA_DIR", "data")
    TOP_K: int = int(os.getenv("TOP_K", "3"))


settings = Settings()