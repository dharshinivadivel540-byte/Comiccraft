from app.schemas import (
    ComicOutline,
    ComicStory,
    PanelOutline,
    PanelStory,
)


def demo_outline(req) -> ComicOutline:
    character = req.character_name
    setting = req.setting
    tone = req.tone
    style = req.art_style

    titles = [
        "The Spark",
        "Into the Unknown",
        "The Warning",
        "The Choice",
        "A New Beginning",
    ]

    descriptions = [
        f"{character} discovers a strange clue in {setting}.",

        f"{character} follows the clue deeper into {setting}.",

        (
            "A mysterious obstacle appears and "
            "changes the mood of the adventure."
        ),

        (
            f"{character} makes a brave decision "
            "that reveals the heart of the story."
        ),

        (
            f"The danger passes and {character} "
            f"sees {setting} in a completely new way."
        ),
    ]

    panels = []

    for i in range(5):
        panels.append(
            PanelOutline(
                panel_number=i + 1,
                title=titles[i],
                scene_description=descriptions[i],
                image_prompt=(
                    f"{style} illustration, "
                    f"{tone} mood, "
                    f"{character} in {setting}, "
                    "cinematic composition, "
                    f"comic panel {i + 1}"
                ),
            )
        )

    return ComicOutline(
        panels=panels
    )


def demo_story(req, outline: ComicOutline) -> ComicStory:
    character = req.character_name

    lines = [
        (
            "A quiet mystery begins.",
            (
                f"{character} notices something impossible "
                "and decides to investigate."
            ),
            "What is that?",
        ),

        (
            "The path grows stranger.",
            (
                f"Every step gives {character} another "
                "reason to turn back, but curiosity wins."
            ),
            "I have to know.",
        ),

        (
            "A warning arrives.",
            (
                "A sudden sign makes the danger clear, "
                "yet the clue points forward."
            ),
            "This is a warning.",
        ),

        (
            "Courage has a cost.",
            (
                f"{character} chooses courage over comfort "
                "and takes the final step."
            ),
            "Then I choose to continue.",
        ),

        (
            "The mystery becomes a memory.",
            (
                f"{character} returns changed, carrying "
                "a story worth telling."
            ),
            "Some adventures begin with one small clue.",
        ),
    ]

    panels = []

    for i, (caption, narration, dialogue) in enumerate(lines):
        panels.append(
            PanelStory(
                panel_number=i + 1,
                caption=caption,
                narration=narration,
                dialogue=dialogue,
            )
        )

    return ComicStory(
        panels=panels
    )