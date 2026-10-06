@echo off

echo ========================================
echo        ComicCraft Setup
echo ========================================

if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

call .venv\Scripts\activate.bat

echo Installing dependencies...

python -m pip install --upgrade pip

pip install -r requirements.txt

if not exist .env (
    copy .env.example .env
)

echo.
echo ========================================
echo Starting ComicCraft...
echo ========================================

uvicorn app.main:app --reload

pause