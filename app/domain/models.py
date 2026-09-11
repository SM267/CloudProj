"""Provider-neutral domain models used by the software factory."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class StageStatus(StrEnum):
    """Lifecycle state of one factory stage."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class FactoryStage(BaseModel):
    """Execution metadata for one stage in the factory pipeline."""

    name: str = Field(min_length=1)
    status: StageStatus = StageStatus.PENDING
    summary: str | None = None
    duration_ms: int | None = Field(default=None, ge=0)
    error: str | None = None
    artifact_ids: list[str] = Field(default_factory=list)


class SoftwarePlan(BaseModel):
    """Structured output of the planning phase."""

    model_config = ConfigDict(extra="forbid")

    requirement: str = Field(min_length=1)
    language: str = Field(min_length=1)
    framework: str = Field(min_length=1)
    stages: list[FactoryStage] = Field(default_factory=list)
    architecture: dict[str, object] = Field(default_factory=dict)
    tasks: list[str] = Field(default_factory=list)
