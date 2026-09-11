"""HTTP endpoints for the software factory."""

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.config import get_settings
from app.services.factory import SoftwareFactory

router = APIRouter()


class PlanRequest(BaseModel):
    requirement: str = Field(min_length=10, max_length=20_000)
    language: str = Field(default="python", min_length=1, max_length=100)
    framework: str = Field(default="fastapi", min_length=1, max_length=100)


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": get_settings().app_name}


@router.get("/api/v1/meta")
async def meta() -> dict[str, str]:
    settings = get_settings()
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }


@router.post("/api/v1/factory/plan")
async def create_plan(request: PlanRequest) -> dict:
    factory = SoftwareFactory()
    plan = await factory.plan(
        requirement=request.requirement,
        language=request.language,
        framework=request.framework,
    )
    return plan.model_dump(mode="json")
