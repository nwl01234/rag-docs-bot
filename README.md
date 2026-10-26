# RAG Docs Bot — локальный бот-ответчик по базе документов

![RAG Docs Bot](.assets/banner.svg)

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![CI](https://img.shields.io/github/actions/workflow/status/nwl01234/rag-docs-bot/ci.yml?label=CI&logo=github)
![License](https://img.shields.io/badge/License-MIT-green)

## Что внутри

| Модуль | Что делает |
|---|---|
| `core/rag.py` | чанкинг документов, TF-IDF индекс, расширение запроса, сборка ответа с источниками |
| `core/eval.py` | оценка качества: golden hit-rate@3, offline A/B (синонимы vs plain), отчёт |
| `app.py` | FastAPI: `POST /api/ask`, `GET /api/health` |
| `data/docs/*.md` | база знаний (примеры: HR-политики, IT-доступы) |
| `demo.py` | 3 вопроса → ответ + источники, офлайн |
| `tests/test_rag.py` | 3 теста: индекс, ответ со ссылкой на документ, честный отказ на miss-вопрос |

## Пайплайн

```
data/docs/*.md
     │  load_docs(): разбр на чанки по заголовкам "## " (заголовок = старт чанка)
     ▼
чанки (doc, chunk_id, text)
     │  build_index(): df(w) по чанкам; vec(w) = tf · log(N/df)   — TF-IDF на чистом Python
     ▼
индекс
     │  search(): топ-3 чанков по сумме весов совпавших слов
     │            запрос расширяется синонимами (SYN-карта: "отпуск" → + отгул, каникулы)
     ▼
answer(): лучший чанк → текст ответа; sources = [{"doc", "score"}, ...]
          score=0 → "в базе нет ответа" (без LLM, без выдумки)
```

TF-IDF собственный, без sklearn/numpy — чтобы индекс работал на любом
контуре без тяжёлых зависимостей. Индекс строится один раз на старте сервера.

## Архитектурный принцип

Ответ **не генерируется** — он извлекается из базы вместе с ссылкой на документ.
Это же ограничение — и фича: у системы нет источника галлюцинаций.

Production-путь: замена поисковой части на embedding-модель
(sentence-transformers) или локальную LLM (Ollama) — `build_index/search` —
это уже тонкий интерфейс, бэкенд меняется без правок API.

## API

```bash
uvicorn app:app --port 8095

curl -X POST localhost:8095/api/ask -H "Content-Type: application/json" \
  -d "{\"q\": \"сколько дней отпуск\"}"
# → {"answer": "Отпуск: основной оплачиваемый отпуск — 28 календарных дней...",
#    "sources": [{"doc": "hr_policy", "score": 0.87}, ...], "mode": "offline"}

curl localhost:8095/api/health
# → {"status": "ok", "chunks": 6, "mode": "offline"}
```

## Запуск

```bash
pip install -r requirements.txt
python demo.py      # 3 сценария: уточнение по базе → miss-вопрос → honest отказ
pytest tests/ -q    # 3 теста
```

Своя база: положи .md-файлы в `data/docs/` (разбивка — по заголовкам `## `).
Индекс строится автоматически при импорте `app.py`.

## Что дальше

- [ ] Telegram-бот: тот же движок в рабочем чате команды
- [ ] Бэкенд поиска на sentence-transformers / Ollama (одна замена интерфейса)
- [ ] Оценка качества: набор эталонных вопрос→документ пар, метрика hit-rate@3
- [ ] Инкрементальное обновление индекса без рестарта

MIT License
