# RAG Docs Bot — AI-бот по корпоративным документам с цитатами

![RAG Docs Bot](.assets/banner.svg)

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![CI](https://img.shields.io/github/actions/workflow/status/nwl01234/rag-docs-bot/ci.yml?label=CI&logo=github)
![License](https://img.shields.io/badge/License-MIT-green)

## Почему это болит у работодателей

HR-отдел завален ежедневными вопросами: «Сколько дней отпуска?», «Кто
оплачивает больничный?». Бухгалтерия и IT тратят ~70% времени на эти ответы,
перемирая одни и те же справки. AI-вакансии («Python Backend/AI voice agents»,
«AI Engineer») прямо требуют: бот по внутренней базе знаний — но готовые
решения галлюцинируют и выдумывают ответы.

RAG Docs Bot решает это: ответы **только из базы docs**, каждый ответ
сопровождается ссылкой на источник → точное цитирование из документа. Если
ответа в базе нет — бот честный: «в базе нет ответа», не выдумывает.

## Как работает

```
Вопрос («сколько дней отпуск»)
        │
        ▼
Нормализация + расширение синонимами (SYN-карта в core/rag.py)
        │        напр. "отпуск" → + "отгул каникулы"
        ▼
TF-IDF поиск по чанкам (полностью офлайн, на чистом Python)
        │
        ▼
Топ-3 чанков по score ──► лучший → сборка ответа
                           • answer  = текст чанка (первое предложение)
                           • sources = [{"doc": "hr_policy", "score": 0.87}, ...]
                           • если score=0 → честный "в базе нет ответа" (не выдумка)
```

Индекс — TF-IDF на чанках docs (реализован без numpy/sklearn, всё вручную).
Перефразирование и фасонирование ответа работает офлайн, без интернета.
Production-путь: подмена поисковика на embedding-модель (sentence-transformers)
или Ollama — интерфейс `build_index/search` уже отвязан от реализации.

## API

```bash
uvicorn app:app --port 8095
curl -X POST localhost:8095/api/ask -H "Content-Type: application/json" \
  -d "{\"q\": \"сколько дней отпуск\"}"
# → {"answer": "Отпуск Основной оплачиваемый отпуск — 28 календарных ...",
#    "sources": [{"doc": "hr_policy", "score": 0.87}, ...], "mode": "offline"}
```

## Быстрый старт

```bash
pip install -r requirements.txt
python demo.py     # 3 вопроса → ответ + источники, всё офлайн
pytest tests/ -q   # 3 теста: индекс, ответ с источником, честный отказ
```

Своя база: положить .md-файлы в `data/docs/` (разметка `## Человекочитаемый заголовок`
= начало чанка), индекс строится на старте сервера автоматически.

## Честность демо-режима

Поиск и сборка ответа полностью рабочие (TF-IDF, офлайн, цитирование).
LLM-перефраз (Ollama/sentence-transformers) — точка расширения, интерфейс
не меняется. Тесты проверяют реальные кейсы: вопрос / miss-вопрос / cite.

## Стек

Python 3.11 · FastAPI · Pydantic · TF-IDF на чистом Python · Telegram Bot API (roadmap) · pytest · GitHub Actions CI

## Что дальше

- [ ] Telegram-бот: тот же движок в рабочем чате команды
- [ ] sentence-transformers / Ollama как searchable-бэкенд (одна замена)
- [ ] Оценка качества: набор эталонных Q→doc пар, метрика hit-rate

MIT License
