from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    app_name: str = "ComicCraft"

    # Gemini
    gemini_api_key: str | None = None
    gemini_flash_model: str = "gemini-2.5-flash"
    gemini_pro_model: str = "gemini-2.5-pro"

    # Hugging Face
    hf_token: str | None = None
    hf_image_model: str = "black-forest-labs/FLUX.1-schnell"
    hf_provider: str = "auto"

    # Application
    demo_mode: bool = True
    max_panels: int = 5

    # Image size
    image_width: int = 768
    image_height: int = 1024

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def templates_dir(self) -> Path:
        return BASE_DIR / "template"

    @property
    def static_dir(self) -> Path:
        return BASE_DIR / "static"

    @property
    def panels_dir(self) -> Path:
        return self.static_dir / "panels"

    @property
    def exports_dir(self) -> Path:
        return self.static_dir / "exports"

    def ensure_dirs(self) -> None:
        self.panels_dir.mkdir(parents=True, exist_ok=True)
        self.exports_dir.mkdir(parents=True, exist_ok=True)


def get_settings() -> Settings:
    settings = Settings()
    settings.ensure_dirs()
    return settings