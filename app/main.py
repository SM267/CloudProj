"""FastAPI application entry point."""

from fastapi import FastAPI

from app.api.routes import router
from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title="CloudProj",
    version=settings.app_version,
    description="Cloud-agnostic AI software development factory.",
)
app.include_router(router)
