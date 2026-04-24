from functools import lru_cache
from pathlib import Path
from typing import Annotated

from pydantic import AliasChoices, Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


API_DIR = Path(__file__).resolve().parents[2]
REPO_ROOT = Path(__file__).resolve().parents[4]


def _split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


class Settings(BaseSettings):
    app_name: str = "BiasharaMind API"
    app_version: str = "0.1.0"
    api_v1_prefix: str = ""
    cors_origins: Annotated[list[str], NoDecode] = ["http://localhost:3000"]
    debug: bool = False
    database_url: str | None = Field(
        default=None,
        validation_alias=AliasChoices("DATABASE_URL", "API_DATABASE_URL"),
    )
    database_echo: bool = False
    supabase_url: str | None = Field(
        default=None,
        validation_alias=AliasChoices("SUPABASE_URL", "API_SUPABASE_URL"),
    )
    supabase_service_role_key: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "SUPABASE_SERVICE_ROLE_KEY",
            "API_SUPABASE_SERVICE_ROLE_KEY",
        ),
    )
    ai_interpretation_provider: str = "disabled"
    ai_interpretation_endpoint: str | None = None
    ai_interpretation_api_key: str | None = None
    ai_interpretation_model: str | None = None
    ai_interpretation_timeout_seconds: int = 20

    model_config = SettingsConfigDict(
        env_prefix="API_",
        env_file=(REPO_ROOT / ".env", API_DIR / ".env"),
        extra="ignore",
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return _split_csv(value)
        return value

    @field_validator("database_url", mode="before")
    @classmethod
    def normalize_database_url(cls, value: str | None) -> str | None:
        if value is None:
            return None

        normalized = value.strip()
        if not normalized:
            return None
        if normalized.startswith("postgresql+psycopg://"):
            return normalized
        if normalized.startswith("postgresql://"):
            return normalized.replace("postgresql://", "postgresql+psycopg://", 1)
        if normalized.startswith("postgres://"):
            return normalized.replace("postgres://", "postgresql+psycopg://", 1)
        return normalized

    @field_validator(
        "supabase_url",
        "supabase_service_role_key",
        "ai_interpretation_endpoint",
        "ai_interpretation_api_key",
        "ai_interpretation_model",
        mode="before",
    )
    @classmethod
    def normalize_optional_string(cls, value: str | None) -> str | None:
        if value is None:
            return None

        normalized = value.strip()
        return normalized or None


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
