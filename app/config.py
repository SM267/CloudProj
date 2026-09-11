"""Application configuration loaded from environment variables."""

from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for CloudProj.

    Secrets are intentionally read only from environment variables and are never
    included in API responses or logs.
    """

    app_name: str = "CloudProj"
    app_version: str = "0.2.0"
    environment: str = "development"
    default_llm_provider: str = "stub"
    default_cloud_provider: str = "docker"
    log_level: str = "INFO"

    llm_timeout_seconds: float = Field(default=30.0, gt=0, le=300)
    llm_max_retries: int = Field(default=2, ge=0, le=5)

    openai_api_key: SecretStr | None = None
    openai_model: str = "gpt-4o-mini"
    openai_base_url: str = "https://api.openai.com/v1"

    gemini_api_key: SecretStr | None = None
    gemini_model: str = "gemini-2.5-flash"
    gemini_base_url: str = "https://generativelanguage.googleapis.com/v1beta"

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="CLOUDPROJ_",
        extra="ignore",
        case_sensitive=False,
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the cached application settings instance."""

    return Settings()
