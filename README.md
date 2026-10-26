# RAG Docs Bot — AI-бот по корпоративным документам с ссылками на источники

![RAG Docs Bot](.assets/banner.svg)

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

Бот отвечает на вопросы сотрудников по базе документов компании:
**поиск по смыслу (TF-IDF + расширение запроса синонимами) → сжатие → ответ с цитатами**.
Работает полностью офлайн; локальная LLM (Ollama) подключается одним флагом для перефразирования.

## Почему это нужно

- Сотрудники задают одни и те же вопросы в чат бухгалтерии/IT → бот снимает 70% нагрузки
- Ответ всегда **со ссылкой на источник** — минимум галлюцинаций
- Локальный контур: документы не покидают контур компании

## Быстрый старт

```bash
pip install -r requirements.txt
uvicorn app:app --port 8095
```

```bash
curl -X POST localhost:8095/api/ask -H "Content-Type: application/json" ^
  -d "{\"q\": \"сколько дней отпуск\"}"
```

## Telegram

`POST /api/telegram/webhook` — тот же движок для бота в рабочем чате.

## Архитектура

```
вопрос ──► нормализация ──► TF-IDF поиск ──► топ-3 чанков ──► сборка ответа
                                   │                        │
                            (Ollama / Локальная LLM) ──► перефраз, кавычки
```

## Стек

Python 3.11 · FastAPI · TF-IDF (реализован на чистом Python) · Telegram Bot API · Docker

MIT License
