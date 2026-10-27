@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo [rag-docs-bot] запуск на http://127.0.0.1:8000
if not exist ".venv\Scripts\python.exe" (
  python -m venv .venv
  .venv\Scripts\pip install -q -r requirements.txt
)
start "" http://127.0.0.1:8000/docs
.venv\Scripts\python -m uvicorn app:app --port 8000
