"""Core orchestration service for the AI software factory."""

from app.domain.models import FactoryStage, SoftwarePlan, StageStatus
from app.providers.llm import LLMMessage, LLMProvider, StubLLMProvider


class SoftwareFactory:
    """Coordinates provider-neutral workflow stages."""

    def __init__(self, llm: LLMProvider | None = None) -> None:
        self.llm = llm or StubLLMProvider()

    async def plan(self, requirement: str, language: str, framework: str) -> SoftwarePlan:
        architecture = {
            "style": "modular-service",
            "api": "REST",
            "language": language,
            "framework": framework,
            "provider_neutral": True,
        }

        tasks = [
            "Define domain model and API contract",
            "Implement application service layer",
            "Add persistence abstraction",
            "Add unit and integration tests",
            "Containerize application",
            "Validate build in an isolated executor",
        ]

        stages = [
            FactoryStage(name="requirements", status=StageStatus.SUCCEEDED, summary="Requirement accepted"),
            FactoryStage(name="architecture", status=StageStatus.SUCCEEDED, summary="Initial architecture produced"),
            FactoryStage(name="planning", status=StageStatus.SUCCEEDED, summary="Implementation tasks created"),
            FactoryStage(name="code_generation", status=StageStatus.PENDING),
            FactoryStage(name="testing", status=StageStatus.PENDING),
            FactoryStage(name="review", status=StageStatus.PENDING),
        ]

        await self.llm.generate([
            LLMMessage(role="system", content="You are the planning stage of a software factory."),
            LLMMessage(role="user", content=requirement),
        ])

        return SoftwarePlan(
            requirement=requirement,
            language=language,
            framework=framework,
            stages=stages,
            architecture=architecture,
            tasks=tasks,
        )
