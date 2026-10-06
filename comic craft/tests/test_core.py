from pathlib import Path

from PIL import Image

import app.config as config

from app.config import Settings

from app.schemas import PromptRequest

from app.services.demo_data import (
    demo_outline,
    demo_story,
)

from app.services.image_generator import ImageGenerator
from app.services.layout_builder import (
    build_comic_layout,
)

from app.services.exporters import (
    save_pdf,
)

from app.services.pipeline import generate_comic


def test_demo_pipeline_builds_five_panels(
    tmp_path,
):

    config.BASE_DIR = tmp_path

    settings = Settings(
        demo_mode=True
    )

    settings.ensure_dirs()

    request = PromptRequest(
        story_prompt=(
            "A fox finds a hidden library"
        ),
        character_name="Milo",
    )

    outline = demo_outline(
        request
    )

    story = demo_story(
        request,
        outline,
    )

    image_paths = []

    for panel in outline.panels:

        file = (
            settings.panels_dir
            / f"p{panel.panel_number}.png"
        )

        Image.new(
            "RGB",
            (200, 300),
            "white",
        ).save(file)

        image_paths.append(
            f"/static/panels/{file.name}"
        )

    layout = build_comic_layout(
        outline,
        story,
        image_paths,
    )

    assert len(layout) == 5

    pdf_url = save_pdf(
        settings,
        "Test Comic",
        layout,
    )

    pdf_file = (
        settings.exports_dir
        / Path(pdf_url).name
    )

    assert pdf_file.exists()


def test_request_validation():

    request = PromptRequest(
        story_prompt="hello"
    )

    assert request.character_name == "Alex"

    assert (
        request.setting
        == "enchanted forest"
    )

    assert (
        request.tone
        == "dramatic"
    )

    assert (
        request.art_style
        == "comic book"
    )


def test_generate_comic_respects_demo_mode_setting(tmp_path):
    config.BASE_DIR = tmp_path
    settings = Settings(demo_mode=True)
    settings.ensure_dirs()

    result = generate_comic(
        PromptRequest(
            story_prompt="A fox discovers a hidden library",
            character_name="Milo",
        ),
        settings,
    )

    assert result["demo_mode"] is True
    assert (settings.panels_dir / "panel_1_test.png").exists() or len(result["layout"]) == 5


def test_image_generator_creates_missing_panel_dir(tmp_path):
    config.BASE_DIR = tmp_path
    settings = Settings(demo_mode=True)
    generator = ImageGenerator(settings)

    output = generator.generate_image("Test prompt", 1)

    assert output.startswith("/static/panels/")
    assert (settings.panels_dir / Path(output).name).exists()