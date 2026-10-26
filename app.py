# -*- coding: utf-8 -*-
"""RAG Docs Bot API: вопросы по корпоративным документам с цитатами источников."""
from fastapi import FastAPI
from pydantic import BaseModel

from core.rag import answer, build_index, load_docs

app = FastAPI(title="RAG Docs Bot", version="1.0.0")
INDEX = build_index(load_docs())


class Q(BaseModel):
    q: str


@app.get("/api/health")
def health():
    return {"status": "ok", "chunks": len(INDEX["docs"]), "mode": "offline"}


@app.post("/api/ask")
def ask(q: Q):
    return answer(q.q, INDEX)
