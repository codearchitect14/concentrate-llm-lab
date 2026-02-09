import os
from typing import Literal

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):

    concentrate_api_key: str
    concentrate_api_base_url: str = "https://api.concentrate.ai/v1"
    openai_models: str = "openai/gpt-4o-mini"
    anthropic_models: str = "anthropic/claude-haiku-3"

    class Config:

        env_file = ".env"
        case_sensitive = False


settings = Settings(
    concentrate_api_key=os.getenv("CONCENTRATE_API_KEY", ""),
    concentrate_api_base_url=os.getenv("CONCENTRATE_API_BASE_URL", "https://api.concentrate.ai/v1"),
    openai_models=os.getenv("OPENAI_MODELS", "openai/gpt-4o-mini"),
    anthropic_models=os.getenv("ANTHROPIC_MODELS", "anthropic/claude-haiku-3"),
)


def parse_models(model_string: str) -> list[str]:
    return [model.strip() for model in model_string.split(",") if model.strip()]


OPENAI_MODELS = parse_models(settings.openai_models)
ANTHROPIC_MODELS = parse_models(settings.anthropic_models)

OPENAI_MODELS_DICT = {
    model.split("/")[-1]: model for model in OPENAI_MODELS
}

ANTHROPIC_MODELS_DICT = {
    model.split("/")[-1]: model for model in ANTHROPIC_MODELS
}

Provider = Literal["openai", "anthropic"]
