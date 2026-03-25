from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "BiasharaMind Worker"
    environment: str = "development"
    graph_name: str = "business_assessment_v1"
    debug: bool = False

    model_config = SettingsConfigDict(
        env_prefix="WORKER_",
        env_file=".env",
        extra="ignore",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
