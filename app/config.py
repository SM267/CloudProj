"""Application configuration."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables."""

    app_name: str = "CloudProj"
    app_version: str = "0.1.0"
    environment: str = "development"
    default_llm_provider: str = "stub"
    default_cloud_provider: str = "docker"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="CLOUDPROJ_", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
