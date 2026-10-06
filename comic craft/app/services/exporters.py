from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from fpdf import FPDF, XPos, YPos
from PIL import Image

from app.config import Settings


def _local_image(
    settings: Settings,
    image_url: str,
) -> Path:

    name = Path(
        urlparse(image_url).path
    ).name

    path = settings.panels_dir / name

    if not path.exists():
        raise FileNotFoundError(
            f"Image not found: {path}"
        )

    return path


def save_pdf(
    settings: Settings,
    title: str,
    layout: list[dict],
) -> str:

    settings.ensure_dirs()

    filename = (
        "comic_"
        + datetime.now().strftime(
            "%Y%m%d_%H%M%S_%f"
        )
        + ".pdf"
    )

    output = (
        settings.exports_dir / filename
    )

    pdf = FPDF(
        orientation="P",
        unit="mm",
        format="A4",
    )

    pdf.set_auto_page_break(
        auto=True,
        margin=15,
    )

    for panel in layout:

        pdf.add_page()

        # Panel title
        pdf.set_font(
            "Helvetica",
            "B",
            20,
        )

        pdf.cell(
            0,
            12,
            (
                f"Panel "
                f"{panel['panel_number']}: "
                f"{panel['title']}"
            ),
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
        )

        # Image
        image_path = _local_image(
            settings,
            panel["image_url"],
        )

        with Image.open(image_path) as image:
            image_width, image_height = (
                image.size
            )

        max_width = 180
        max_height = 120

        ratio = min(
            max_width / image_width,
            max_height / image_height,
        )

        display_width = (
            image_width * ratio
        )

        display_height = (
            image_height * ratio
        )

        x = (
            210 - display_width
        ) / 2

        y = 30

        pdf.image(
            str(image_path),
            x=x,
            y=y,
            w=display_width,
            h=display_height,
        )

        # Text starts below image
        pdf.set_y(
            y + display_height + 8
        )

        # Scene
        pdf.set_font(
            "Helvetica",
            "I",
            11,
        )

        pdf.multi_cell(
            180,
            7,
            panel["scene_description"],
        )

        pdf.ln(2)

        # Caption
        pdf.set_font(
            "Helvetica",
            "B",
            11,
        )

        pdf.multi_cell(
            180,
            7,
            "Caption: "
            + panel["caption"],
        )

        # Narration
        pdf.set_font(
            "Helvetica",
            "",
            11,
        )

        pdf.multi_cell(
            180,
            7,
            "Narration: "
            + panel["narration"],
        )

        # Dialogue
        pdf.set_font(
            "Helvetica",
            "B",
            11,
        )

        pdf.multi_cell(
            180,
            7,
            "Dialogue: "
            + panel["dialogue"],
        )

    pdf.output(str(output))

    return (
        f"/static/exports/{filename}"
    )