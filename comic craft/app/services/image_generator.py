from pathlib import Path
import re

from PIL import Image, ImageDraw, ImageFont

from app.config import Settings


def safe_name(text: str) -> str:
    name = re.sub(
        r"[^a-zA-Z0-9_-]+",
        "_",
        text,
    )

    name = name.strip("_")

    return name[:60] or "panel"


class ImageGenerator:

    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = None

        if settings.hf_token:
            try:
                from huggingface_hub import InferenceClient

                self.client = InferenceClient(
                    provider=settings.hf_provider,
                    api_key=settings.hf_token,
                )

            except ImportError as exc:
                raise RuntimeError(
                    "huggingface-hub is not installed. "
                    "Run: pip install -r requirements.txt"
                ) from exc

    def generate_image(
        self,
        prompt: str,
        panel_number: int,
    ) -> str:

        self.settings.ensure_dirs()

        output = (
            self.settings.panels_dir
            / (
                f"panel_{panel_number}_"
                f"{safe_name(prompt)}.png"
            )
        )

        # Real Hugging Face generation
        if self.client:

            try:
                image = self.client.text_to_image(
                    prompt,
                    model=self.settings.hf_image_model,
                    width=self.settings.image_width,
                    height=self.settings.image_height,
                )

                image.save(output)

                return (
                    f"/static/panels/{output.name}"
                )

            except Exception:

                if not self.settings.demo_mode:
                    raise

        # Demo image
        if not self.settings.demo_mode:
            raise RuntimeError(
                "HF_TOKEN is not configured or "
                "image generation failed."
            )

        self._create_demo_image(
            output,
            prompt,
            panel_number,
        )

        return (
            f"/static/panels/{output.name}"
        )

    def _create_demo_image(
        self,
        output: Path,
        prompt: str,
        panel_number: int,
    ) -> None:

        width = self.settings.image_width
        height = self.settings.image_height

        image = Image.new(
            "RGB",
            (width, height),
            (245, 235, 210),
        )

        draw = ImageDraw.Draw(image)

        # Border
        draw.rectangle(
            (
                20,
                20,
                width - 20,
                height - 20,
            ),
            outline=(25, 25, 25),
            width=8,
        )

        # Head
        draw.ellipse(
            (
                width // 2 - 130,
                180,
                width // 2 + 130,
                440,
            ),
            outline=(25, 25, 25),
            width=8,
        )

        # Body
        draw.line(
            (
                width // 2,
                440,
                width // 2,
                700,
            ),
            fill=(25, 25, 25),
            width=10,
        )

        # Arms
        draw.line(
            (
                width // 2,
                520,
                width // 2 - 150,
                620,
            ),
            fill=(25, 25, 25),
            width=10,
        )

        draw.line(
            (
                width // 2,
                520,
                width // 2 + 150,
                620,
            ),
            fill=(25, 25, 25),
            width=10,
        )

        # Legs
        draw.line(
            (
                width // 2,
                700,
                width // 2 - 120,
                900,
            ),
            fill=(25, 25, 25),
            width=10,
        )

        draw.line(
            (
                width // 2,
                700,
                width // 2 + 120,
                900,
            ),
            fill=(25, 25, 25),
            width=10,
        )

        font = ImageFont.load_default()

        draw.text(
            (45, 45),
            f"COMICCRAFT • PANEL {panel_number}",
            fill=(20, 20, 20),
            font=font,
        )

        prompt_text = prompt[:220]

        draw.text(
            (45, height - 120),
            prompt_text,
            fill=(20, 20, 20),
            font=font,
        )

        image.save(output)