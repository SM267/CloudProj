"""Core orchestration service for the AI software factory."""

from __future__ import annotations

from app.domain.models import FactoryStage, SoftwarePlan, StageStatus
from app.providers.llm import LLMMessage, LLMProvider, build_llm_provider


class SoftwareFactory:
    """Coordinate provider-neutral planning stages.

    The service owns workflow semantics; concrete model SDKs remain inside the
    provider layer. This makes the pipeline deterministic and easy to test with
    a fake provider.
    """

    def __init__(self, llm: LLMProvider | None = None) -> None:
        self.llm = llm or build_llm_provider()

    async def plan(self, requirement: str, language: str, framework: str) -> SoftwarePlan:
        """Create an initial architecture and implementation plan.

        The current MVP keeps the baseline plan deterministic while still calling
        the configured provider. Later stages can replace individual deterministic
        artifacts with validated structured model output without changing the API.
        """

        stages = [
            FactoryStage(name="requirements", status=StageStatus.SUCCEEDED, summary="Requirement accepted"),
            FactoryStage(name="architecture", status=StageStatus.SUCCEEDED, summary="Initial architecture produced"),
            FactoryStage(name="planning", status=StageStatus.SUCCEEDED, summary="Implementation tasks created"),
            FactoryStage(name="code_generation"),
            FactoryStage(name="testing"),
            FactoryStage(name="review"),
        ]

        # The provider call verifies the selected adapter and gives future stages
        # a stable insertion point without making generated text part of the API
        # contract yet.
        await self.llm.generate(
            [
                LLMMessage(
                    role="system",
                    content="You are the planning stage of a software factory. Return concise analysis.",
                ),
                LLMMessage(role="user", content=requirement),
            ]
        )

        architecture = {
            "style": "modular-service",
            "api": "REST",
            "language": language,
            "framework": framework,
            "provider_neutral": True,
            "deployment_target": "container",
        }
        tasks = [
            "Define the domain model and API contract",
            "Implement the application service layer",
            "Add persistence behind an abstraction",
            "Add unit and integration tests",
            "Containerize the application",
            "Validate the build in an isolated executor",
        ]
        return SoftwarePlan(
            requirement=requirement,
            language=language,
            framework=framework,
            stages=stages,
            architecture=architecture,
            tasks=tasks,
        )
