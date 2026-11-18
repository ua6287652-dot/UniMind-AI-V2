# UniMind AI V2 — Agentic University Knowledge Assistant

Separate Agentic RAG application using Streamlit, LangGraph, Groq, HuggingFace embeddings and FAISS.

## Windows setup
```powershell
py -3.12 -m venv venv
.\\venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```
Add your Groq API key to `.env`, then run:
```powershell
python -m streamlit run app.py
```

## Streamlit Cloud secrets
```toml
GROQ_API_KEY = "your_actual_key"
GROQ_MODEL = "openai/gpt-oss-120b"
```
Main file: `app.py`.

## V1 integration
V1 remains unchanged. V2 intentionally creates its own FAISS index instead of assuming the old index format. Upload the same source PDFs/DOCX/TXT files into V2 using Upload Knowledge. This makes the new app independently testable and deployable.

## Limitations
Scanned PDFs need OCR. Local Streamlit Cloud storage is not durable across all restarts/redeployments; production requires persistent storage. The agent cannot submit applications, make payments or modify student records. Greenfield sample documents are fictional.
