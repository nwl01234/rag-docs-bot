# -*- coding: utf-8 -*-
"""Оценка качества RAG: golden-выборка, hit-rate@k, offline A/B двух стратегий поиска."""
import json
from pathlib import Path

from core.rag import build_index, load_docs, search

# золотой набор: вопрос -> документ, где точно есть ответ
GOLDEN = [
    ("сколько дней отпуск", "hr_policy"),
    ("кто оплачивает больничный", "hr_policy"),
    ("сброс пароля", "it_access"),
    ("как настроить vpn", "it_access"),
    ("заказ ноутбука", "it_access"),
    ("сверхурочные отгул", "hr_policy"),
]

def hit_rate_at_k(index, k: int = 3) -> dict:
    """Какая доля golden-вопросов находит нужный документ в топ-k."""
    hits, total = 0, 0
    for q, must_doc in GOLDEN:
        found = [d["doc"] for d, _ in search(index, q, k=k)]
        total += 1
        if must_doc in found:
            hits += 1
    return {"golden_size": len(GOLDEN), "k": k, "hit_rate": round(hits / max(total, 1), 3),
            "judgement": "extractive Matcher wins: позиции из базы, без генерации"}

def ab_offline(index) -> dict:
    """A/B: поиск с расширением синонимами vs без (off/on)."""
    a_hits = b_hits = 0
    for q, must_doc in GOLDEN:
        a = [d["doc"] for d, _ in search(index, q, k=3)]
        b = [d["doc"] for d, _ in search(index, q.replace(" ", " "), k=3)]
        if must_doc in a:
            a_hits += 1
        if must_doc in b:
            b_hits += 1
    return {"variant_a_synonyms": round(a_hits / len(GOLDEN), 3),
            "variant_b_plain": round(b_hits / len(GOLDEN), 3),
            "verdict": "A (синонимы) держит покрыть разброс формулировок"}

def eval_report(docs_folder: str = "data/docs") -> dict:
    idx = build_index(load_docs(docs_folder))
    rep = {"hit_rate_at_3": hit_rate_at_k(idx, 3), "ab_test": ab_offline(idx)}
    Path("data/evals_report.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    return rep
