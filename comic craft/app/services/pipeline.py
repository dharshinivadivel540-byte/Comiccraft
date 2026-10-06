from app.config import Settings

from app.services.gemini_flash import (
    GeminiFlashService,
)

from app.services.gemini_pro import (
    GeminiProService,
)

from app.services.image_generator import (
    ImageGenerator,
)

from app.services.layout_builder import (
    build_comic_layout,
)

from app.services.exporters import (
    save_pdf,
)


def generate_comic(
    request,
    settings: Settings,
):

    # Step 1
    # Generate structured five-panel outline
    outline = GeminiFlashService(
        settings
    ).generate_outline(request)

    # Step 2
    # Generate narration and dialogue
    story = GeminiProService(
        settings
    ).generate_story(
        request,
        outline,
    )

    # Step 3
    # Generate images
    image_generator = ImageGenerator(
        settings
    )

    image_paths = []

    for panel in outline.panels:

        image_path = (
            image_generator.generate_image(
                panel.image_prompt,
                panel.panel_number,
            )
        )

        image_paths.append(
            image_path
        )

    # Step 4
    # Combine story and images
    layout = build_comic_layout(
        outline,
        story,
        image_paths,
    )

    # Step 5
    # Generate title
    title = (
        f"{request.character_name}'s "
        "Comic Adventure"
    )

    # Step 6
    # Export PDF
    pdf_url = save_pdf(
        settings,
        title,
        layout,
    )

    # Determine whether demo content was used
    ai_mode = (
        bool(settings.gemini_api_key)
        and bool(settings.hf_token)
    )

    return {
        "title": title,
        "layout": layout,
        "pdf_url": pdf_url,
        "demo_mode": not ai_mode,
    }