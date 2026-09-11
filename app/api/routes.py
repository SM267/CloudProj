"""HTTP API for the CloudProj software factory."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.config import get_settings
from app.providers.llm import LLMProvider, build_llm_provider
from app.services.factory import SoftwareFactory

router = APIRouter()


class PlanRequest(BaseModel):
    """Request body for creating a software plan."""

    requirement: str = Field(min_length=10, max_length=20_000)
    language: str = Field(default="python", min_length=1, max_length=100)
    framework: str = Field(default="fastapi", min_length=1, max_length=100)
    llm_provider: str | None = Field(default=None, min_length=1, max_length=30)


def get_factory(provider: str | None = None) -> SoftwareFactory:
    """Construct a factory using the requested or configured LLM provider."""

    return SoftwareFactory(llm=build_llm_provider(provider))


@router.get("/health")
async def health() -> dict[str, str]:
    """Return a lightweight liveness response."""

    return {"status": "ok", "service": get_settings().app_name}


@router.get("/api/v1/meta")
async def meta() -> dict[str, str]:
    """Return non-secret service metadata."""

    settings = get_settings()
    return {"name": settings.app_name, "version": settings.app_version, "environment": settings.environment}


@router.post("/api/v1/factory/plan")
async def create_plan(request: PlanRequest) -> dict:
    """Generate a provider-neutral software plan from a requirement."""

    try:
        factory = get_factory(request.llm_provider)
        plan = await factory.plan(request.requirement, request.language, request.framework)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        # Avoid exposing provider credentials, URLs, or upstream response bodies.
        raise HTTPException(status_code=502, detail="LLM provider request failed") from exc
    return plan.model_dump(mode="json")
