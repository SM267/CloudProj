"""Unit tests for provider contracts and adapters."""

import pytest

from app.config import Settings
from app.providers.cloud import DeploymentRequest, DockerCloudProvider
from app.providers.llm import (
    GeminiProvider,
    LLMMessage,
    LLMProviderError,
    OllamaProvider,
    OpenAIProvider,
    StubLLMProvider,
    build_llm_provider,
)


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
async def test_stub_llm_json_contract() -> None:
    class JsonStub(StubLLMProvider):
        async def generate(self, messages: list[LLMMessage]) -> str:
            return '{"ok": true}'

    assert await JsonStub().generate_json([LLMMessage(role="user", content="test")]) == {"ok": True}


@pytest.mark.asyncio
async def test_invalid_json_is_rejected() -> None:
    class BadStub(StubLLMProvider):
        async def generate(self, messages: list[LLMMessage]) -> str:
            return "not-json"

    with pytest.raises(LLMProviderError):
        await BadStub().generate_json([LLMMessage(role="user", content="test")])


def test_provider_factory() -> None:
    settings = Settings(default_llm_provider="stub")
    assert isinstance(build_llm_provider(settings=settings), StubLLMProvider)
    assert isinstance(build_llm_provider("openai", settings), OpenAIProvider)
    assert isinstance(build_llm_provider("gemini", settings), GeminiProvider)
    assert isinstance(build_llm_provider("ollama", settings), OllamaProvider)


def test_unknown_provider_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unsupported LLM provider"):
        build_llm_provider("unknown")


@pytest.mark.asyncio
async def test_openai_requires_credentials() -> None:
    provider = OpenAIProvider(Settings(openai_api_key=None))
    with pytest.raises(LLMProviderError, match="OPENAI_API_KEY"):
        await provider.generate([LLMMessage(role="user", content="hello")])


@pytest.mark.asyncio
async def test_gemini_requires_credentials() -> None:
    provider = GeminiProvider(Settings(gemini_api_key=None))
    with pytest.raises(LLMProviderError, match="GEMINI_API_KEY"):
        await provider.generate([LLMMessage(role="user", content="hello")])


@pytest.mark.asyncio
async def test_docker_provider_is_non_destructive_planner() -> None:
    provider = DockerCloudProvider()
    result = await provider.deploy(
        DeploymentRequest(project_name="demo", artifact_path="./dist")
    )
    assert result.provider == "docker"
    assert result.status == "planned"
