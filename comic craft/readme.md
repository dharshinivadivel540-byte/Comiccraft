# ComicCraft

ComicCraft is an AI-powered comic story creator.

It converts a user idea into a five-panel comic containing:

- Story outline
- Scene descriptions
- Narration
- Dialogue
- AI-generated illustrations
- PDF export


## Architecture

Frontend:

- HTML
- CSS
- JavaScript
- Jinja2

Backend:

- Python
- FastAPI
- Uvicorn
- Pydantic

AI:

- Google Gemini
- Hugging Face image generation

Export:

- FPDF2
- Pillow


## Project Flow

User Input

↓

Gemini Flash

↓

Five Panel Outline

↓

Gemini Pro

↓

Narration + Dialogue

↓

Hugging Face

↓

Panel Images

↓

Layout Builder

↓

PDF Export

↓

Comic Preview


## Requirements

Python 3.11 or newer is recommended.

Python 3.12 is recommended.


## Installation

Create a virtual environment:

Windows:

python -m venv .venv

Activate:

.venv\Scripts\activate


macOS/Linux:

python3 -m venv .venv

source .venv/bin/activate


Install dependencies:

pip install -r requirements.txt


## Environment Configuration

Copy:

.env.example

to:

.env


Initially keep:

DEMO_MODE=true


This allows the application to run without API keys.


## Run

uvicorn app.main:app --reload


Open:

http://127.0.0.1:8000


API documentation:

http://127.0.0.1:8000/docs


Health check:

http://127.0.0.1:8000/health


## Demo Mode

Demo mode does not call external AI services.

It creates:

- Five sample panels
- Sample narration
- Sample dialogue
- Generated placeholder images
- A real PDF file

This is useful for checking that the application itself works.


## AI Mode

Add your credentials to .env:

GEMINI_API_KEY=your_key

HF_TOKEN=your_token


Then:

DEMO_MODE=false


Restart the server.


## API

POST:

/generate-comic/json


Example JSON:

{
    "story_prompt": "A brave fox explores an enchanted forest",
    "character_name": "Milo",
    "setting": "enchanted forest",
    "tone": "dramatic",
    "art_style": "comic book"
}


GET:

/test-image


Example:

/test-image?prompt=A%20robot%20in%20space


## Testing

Run:

pytest


Expected:

2 tests passed.


## Docker

Create .env first.

Then:

docker compose up --build


Open:

http://localhost:8000


## Troubleshooting

If "python" is not recognized:

Install Python and enable:

Add Python to PATH


If pip is not recognized:

python -m pip install -r requirements.txt


If the port is busy:

uvicorn app.main:app --reload --port 8001


Then open:

http://127.0.0.1:8001


If API credentials are missing:

Use:

DEMO_MODE=true


If real AI generation fails:

Check:

1. GEMINI_API_KEY
2. HF_TOKEN
3. Internet connection
4. Model names
5. Hugging Face provider availability
