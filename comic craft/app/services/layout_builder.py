def build_comic_layout(
    outline,
    story,
    image_paths,
):
    story_by_panel = {
        panel.panel_number: panel
        for panel in story.panels
    }

    layout = []

    for panel in outline.panels:

        story_panel = story_by_panel.get(
            panel.panel_number
        )

        image_url = image_paths[
            panel.panel_number - 1
        ]

        layout.append(
            {
                "panel_number": panel.panel_number,
                "title": panel.title,
                "scene_description": (
                    panel.scene_description
                ),
                "image_prompt": panel.image_prompt,
                "image_url": image_url,
                "caption": (
                    story_panel.caption
                    if story_panel
                    else ""
                ),
                "narration": (
                    story_panel.narration
                    if story_panel
                    else ""
                ),
                "dialogue": (
                    story_panel.dialogue
                    if story_panel
                    else ""
                ),
            }
        )

    return layout