"""Provider-neutral domain models."""

from enum import StrEnum

from pydantic import BaseModel, Field


class StageStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class FactoryStage(BaseModel):
    name: str
    status: StageStatus = StageStatus.PENDING
    summary: str | None = None


class SoftwarePlan(BaseModel):
    requirement: str
    language: str
    framework: str
    stages: list[FactoryStage] = Field(default_factory=list)
    architecture: dict[str, object] = Field(default_factory=dict)
    tasks: list[str] = Field(default_factory=list)
