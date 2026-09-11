import pytest

from app.providers.cloud import DockerCloudProvider, DeploymentRequest
from app.providers.llm import LLMMessage, StubLLMProvider


@pytest.mark.asyncio
async def test_stub_llm_returns_latest_user_message() -> None:
    provider = StubLLMProvider()
    result = await provider.generate(
        [
            LLMMessage(role="system", content="system"),
            LLMMessage(role="user", content="first"),
            LLMMessage(role="user", content="second"),
        ]
    )
    assert result == "second"


@pytest.mark.asyncio
async def test_docker_provider_is_non_destructive_planner() -> None:
    provider = DockerCloudProvider()
    result = await provider.deploy(
        DeploymentRequest(project_name="demo", artifact_path="./dist")
    )
    assert result.provider == "docker"
    assert result.status == "planned"
