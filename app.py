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


@app.get("/api/eval")
def eval_quality():
    """Оценка качества поиска: golden hit-rate@3 + offline A/B синонимы vs plain."""
    from core import eval as rag_eval
    return rag_eval.eval_report()
