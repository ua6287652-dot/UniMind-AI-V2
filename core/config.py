import os, streamlit as st
from dataclasses import dataclass
@dataclass
class Settings:
    groq_api_key:str; groq_model:str; embedding_model:str; index_dir:str
    chunk_size:int; chunk_overlap:int; top_k:int
def get_settings():
    def val(k,d=""):
        try: return st.secrets.get(k,os.getenv(k,d))
        except Exception: return os.getenv(k,d)
    return Settings(val("GROQ_API_KEY"),val("GROQ_MODEL","openai/gpt-oss-120b"),
        val("EMBEDDING_MODEL","sentence-transformers/all-MiniLM-L6-v2"),
        val("FAISS_INDEX_DIR","knowledge_base/faiss_index"),int(val("CHUNK_SIZE","800")),
        int(val("CHUNK_OVERLAP","150")),int(val("TOP_K","5")))
