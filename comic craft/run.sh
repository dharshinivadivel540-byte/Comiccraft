#!/usr/bin/env bash

set -e

echo "========================================"
echo "        ComicCraft Setup"
echo "========================================"

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

source .venv/bin/activate

echo "Installing dependencies..."

python -m pip install --upgrade pip

pip install -r requirements.txt

if [ ! -f ".env" ]; then
    cp .env.example .env
fi

echo ""
echo "========================================"
echo "Starting ComicCraft..."
echo "========================================"

uvicorn app.main:app --reload