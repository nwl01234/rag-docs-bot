# -*- coding: utf-8 -*-
"""Демо: вопросы сотрудников -> ответы с цитатами. python demo.py"""
from core.rag import answer, build_index, load_docs

QS = ["сколько дней отпуск", "не работает вход по паролю", "как получить монитор"]

if __name__ == "__main__":
    idx = build_index(load_docs())
    print(f"индекс: {len(idx['docs'])} чанков")
    for q in QS:
        r = answer(q, idx)
        src = ", ".join(s["doc"] for s in r["sources"]) or "—"
        print(f"\nQ: {q}\nA: {r['answer'][:160]}...\n   источники: {src}")
