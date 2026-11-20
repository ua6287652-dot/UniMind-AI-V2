
from pathlib import Path
import tempfile

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


class KnowledgeBase:
    def __init__(self, cfg):
        self.cfg = cfg
        self.path = Path(cfg.index_dir)
        self.path.mkdir(parents=True, exist_ok=True)

        self.emb = HuggingFaceEmbeddings(
            model_name=cfg.embedding_model
        )

        self.store = None
        self._load()

    def _load(self):
        if (
            (self.path / "index.faiss").exists()
            and (self.path / "index.pkl").exists()
        ):
            try:
                self.store = FAISS.load_local(
                    str(self.path),
                    self.emb,
                    allow_dangerous_deserialization=True,
                )
            except Exception:
                self.store = None

    def add_files(self, uploads):
        docs = []
        errors = []

        with tempfile.TemporaryDirectory() as td:
            for up in uploads:
                p = Path(td) / Path(up.name).name
                p.write_bytes(up.getvalue())

                try:
                    ext = p.suffix.lower()

                    if ext == ".pdf":
                        loaded = PyPDFLoader(str(p)).load()
                    elif ext == ".docx":
                        loaded = Docx2txtLoader(str(p)).load()
                    elif ext == ".txt":
                        loaded = TextLoader(
                            str(p),
                            encoding="utf-8"
                        ).load()
                    else:
                        errors.append(
                            f"{up.name}: Unsupported file format"
                        )
                        continue

                    for doc in loaded:
                        doc.metadata["source"] = p.name
                        docs.append(doc)

                except Exception as e:
                    errors.append(f"{up.name}: {e}")

        if not docs:
            return {
                "chunks": 0,
                "documents": 0,
                "errors": errors or ["No readable text found."],
            }

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.cfg.chunk_size,
            chunk_overlap=self.cfg.chunk_overlap,
            add_start_index=True,
        )

        chunks = splitter.split_documents(docs)

        # Create a new FAISS store OR append to the existing store.
        # Do not add the first upload twice.
        if self.store is None:
            self.store = FAISS.from_documents(
                chunks,
                self.emb
            )
        else:
            self.store.add_documents(chunks)

        self.store.save_local(str(self.path))

        return {
            "chunks": len(chunks),
            "documents": len({
                d.metadata.get("source") for d in docs
            }),
            "errors": errors,
        }

    def search(self, q, k=None):
        if self.store is None:
            self._load()

        return (
            self.store.similarity_search(
                q,
                k=k or self.cfg.top_k
            )
            if self.store
            else []
        )

    def stats(self):
        if self.store is None:
            self._load()

        if not self.store:
            return {
                "ready": False,
                "documents": 0,
                "chunks": 0,
                "files": [],
            }

        vals = self.store.docstore._dict.values()

        files = sorted({
            d.metadata.get("source", "Unknown")
            for d in vals
        })

        return {
            "ready": True,
            "documents": len(files),
            "chunks": self.store.index.ntotal,
            "files": files,
        }
