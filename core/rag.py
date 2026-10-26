# -*- coding: utf-8 -*-
"""RAG-движок: TF-IDF на чистом Python + сборка ответа с цитатами. Офлайн."""
import math, re
from pathlib import Path

def load_docs(folder: str = "data/docs"):
    docs = []
    for p in sorted(Path(folder).glob("*.md")):
        text = p.read_text(encoding="utf-8")
        for i, chunk in enumerate(re.split(r"\n## ", text)):
            if len(chunk) > 40:
                docs.append({"doc": p.stem, "chunk": i, "text": "## " + chunk})
    return docs

def _tok(s: str):
    return re.findall(r"[а-яёa-z0-9]+", s.lower())

def build_index(docs):
    df = {}
    for d in docs:
        for w in set(_tok(d["text"])):
            df[w] = df.get(w, 0) + 1
    N = len(docs)
    tfidf = []
    for d in docs:
        tf = {}
        for w in _tok(d["text"]):
            tf[w] = tf.get(w, 0) + 1
        vec = {w: (c / len(tf)) * math.log(N / df[w]) for w, c in tf.items()}
        tfidf.append(vec)
    return {"docs": docs, "tfidf": tfidf, "df": df, "N": N}

def search(index, query: str, k: int = 3):
    q = _tok(query)
    scores = []
    for i, vec in enumerate(index["tfidf"]):
        s = sum(vec.get(w, 0.0) for w in q)
        scores.append((s, i))
    scores.sort(reverse=True)
    return [(index["docs"][i], s) for s, i in scores[:k] if s > 0]

SYN = {"отпуск": ["отпуск", "отгул", "каникулы"], "зарплата": ["зарплата", "оклад", "аванс"],
       "больнич": ["больничный", "болеть"], "пароль": ["пароль", "доступ", "логин"]}

def expand(query: str) -> str:
    q = query.lower()
    for k, ws in SYN.items():
        if k in q:
            q += " " + " ".join(ws)
    return q

def answer(query: str, index) -> dict:
    hits = search(index, expand(query))
    if not hits:
        return {"answer": "В базе нет ответа. Уточните вопрос или создайте заявку.", "sources": []}
    best = hits[0][0]
    first = re.sub(r"\n+", " ", best["text"].replace("## ", ""))
    srcs = [{"doc": h[0]["doc"], "score": round(h[1], 3)} for h in hits]
    return {"answer": f"{first.strip()[:300]}", "sources": srcs, "mode": "offline"}
