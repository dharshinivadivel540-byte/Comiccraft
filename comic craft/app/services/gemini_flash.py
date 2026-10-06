from app.config import Settings
from app.schemas import (
    ComicOutline,
    PromptRequest,
)

from app.services.demo_data import demo_outline


class GeminiFlashService:

    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = None

        if settings.gemini_api_key:
            try:
                from google import genai

                self.client = genai.Client(
                    api_key=settings.gemini_api_key
                )

            except ImportError as exc:
                raise RuntimeError(
                    "google-genai is not installed. "
                    "Run: pip install -r requirements.txt"
                ) from exc

    def generate_outline(
        self,
        request: PromptRequest,
    ) -> ComicOutline:

        # Demo mode
        if not self.client:

            if self.settings.demo_mode:
                return demo_outline(request)

            raise RuntimeError(
                "GEMINI_API_KEY is not configured."
            )

        prompt = f"""
Create a coherent 5-panel comic outline.

Story idea:
{request.story_prompt}

Main character:
{request.character_name}

Setting:
{request.setting}

Tone:
{request.tone}

Art style:
{request.art_style}

Requirements:

1. Return exactly five panels.
2. Every panel must have a unique title.
3. Every panel needs a concise scene description.
4. Every panel needs a detailed visual image prompt.
5. Keep the main character visually consistent.
6. Make the story have a clear beginning, middle and ending.
7. Do not include markdown.
"""

        from google.genai import types

        response = self.client.models.generate_content(
            model=self.settings.gemini_flash_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.9,
                response_mime_type="application/json",
                response_schema=ComicOutline,
            ),
        )

        return ComicOutline.model_validate_json(
            response.text
        )