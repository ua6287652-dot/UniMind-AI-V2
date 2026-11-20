
import os
import streamlit as st
from dotenv import load_dotenv
from dataclasses import dataclass

# Load environment variables from local .env file
load_dotenv()


@dataclass
class Settings:
    groq_api_key: str
    groq_model: str
    embedding_model: str
    index_dir: str
    chunk_size: int
    chunk_overlap: int
    top_k: int


def get_settings():

    def get_value(key, default=""):
        # Streamlit Cloud Secrets first
        try:
            if key in st.secrets:
                return st.secrets[key]
        except Exception:
            pass

        # Local .env or system environment
        return os.getenv(key, default)

    return Settings(
        groq_api_key=get_value("GROQ_API_KEY"),
        groq_model=get_value(
            "GROQ_MODEL",
            "openai/gpt-oss-120b"
        ),
        embedding_model=get_value(
            "EMBEDDING_MODEL",
            "sentence-transformers/all-MiniLM-L6-v2"
        ),
        index_dir=get_value(
            "FAISS_INDEX_DIR",
            "knowledge_base/faiss_index"
        ),
        chunk_size=int(get_value("CHUNK_SIZE", "800")),
        chunk_overlap=int(get_value("CHUNK_OVERLAP", "150")),
        top_k=int(get_value("TOP_K", "5"))
    )
