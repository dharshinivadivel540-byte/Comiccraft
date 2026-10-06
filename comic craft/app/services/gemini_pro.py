from app.config import Settings

from app.schemas import (
    ComicOutline,
    ComicStory,
    PromptRequest,
)

from app.services.demo_data import demo_story


class GeminiProService:

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

    def generate_story(
        self,
        request: PromptRequest,
        outline: ComicOutline,
    ) -> ComicStory:

        if not self.client:

            if self.settings.demo_mode:
                return demo_story(
                    request,
                    outline,
                )

            raise RuntimeError(
                "GEMINI_API_KEY is not configured."
            )

        outline_json = outline.model_dump_json(
            indent=2
        )

        prompt = f"""
Expand the following five-panel comic outline
into a polished comic script.

User story:
{request.story_prompt}

Character:
{request.character_name}

Setting:
{request.setting}

Tone:
{request.tone}

Art style:
{request.art_style}

OUTLINE:
{outline_json}

For every panel generate:

- a short caption
- narration
- character dialogue

Rules:

1. Keep events consistent with the outline.
2. Do not add panels.
3. Keep the same main character.
4. Make dialogue natural.
5. Keep narration concise.
6. Do not use markdown.
"""

        from google.genai import types

        response = self.client.models.generate_content(
            model=self.settings.gemini_pro_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=1.0,
                response_mime_type="application/json",
                response_schema=ComicStory,
            ),
        )

        return ComicStory.model_validate_json(
            response.text
        )