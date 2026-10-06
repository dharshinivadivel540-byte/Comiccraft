from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import get_settings
from app.schemas import PromptRequest
from app.services.image_generator import ImageGenerator
from app.services.pipeline import generate_comic


router = APIRouter()

settings = get_settings()

templates = Jinja2Templates(
    directory=str(settings.templates_dir)
)


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "demo_mode": settings.demo_mode,
            "error": None,
        },
    )


@router.post("/generate", response_class=HTMLResponse)
async def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
):
    try:
        payload = PromptRequest(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
        )

        result = generate_comic(
            payload,
            settings,
        )

        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context=result,
        )

    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "error": str(exc),
                "demo_mode": settings.demo_mode,
            },
            status_code=500,
        )


@router.post("/generate-comic/json")
async def generate_json(
    payload: PromptRequest,
):
    try:
        return generate_comic(
            payload,
            settings,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@router.get(
    "/export-success",
    response_class=HTMLResponse,
)
async def export_success(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={},
    )


@router.get("/test-image")
async def test_image(
    prompt: str = (
        "A brave fox exploring an enchanted forest, "
        "comic book style"
    ),
):
    try:
        image_url = ImageGenerator(
            settings
        ).generate_image(
            prompt,
            0,
        )

        return {
            "image_url": image_url
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc