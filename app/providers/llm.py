"""Provider-neutral language-model interfaces and HTTP adapters."""

from __future__ import annotations

import asyncio
import json
from abc import ABC, abstractmethod
from typing import Any

import httpx
from pydantic import BaseModel, Field

from app.config import Settings, get_settings


class LLMMessage(BaseModel):
    """A role/content message passed to a chat model."""

    role: str = Field(pattern=r"^(system|user|assistant)$")
    content: str = Field(min_length=1)


class LLMProviderError(RuntimeError):
    """Raised when an LLM provider cannot produce a response."""


class LLMProvider(ABC):
    """Stable application-facing contract for all LLM implementations."""

    name: str

    @abstractmethod
    async def generate(self, messages: list[LLMMessage]) -> str:
        """Generate text from a sequence of chat messages."""
        raise NotImplementedError

    async def generate_json(self, messages: list[LLMMessage]) -> dict[str, Any]:
        """Generate and parse a JSON object using the provider-neutral contract."""

        raw = await self.generate(messages)
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise LLMProviderError("LLM returned invalid JSON") from exc
        if not isinstance(value, dict):
            raise LLMProviderError("LLM JSON response must be an object")
        return value


class StubLLMProvider(LLMProvider):
    """Deterministic implementation used for tests and local development."""

    name = "stub"

    async def generate(self, messages: list[LLMMessage]) -> str:
        """Return the latest user message without making a network request."""

        user_messages = [message.content for message in messages if message.role == "user"]
        return user_messages[-1] if user_messages else "No user requirement supplied."


class _HTTPProvider(LLMProvider):
    """Shared retry, timeout, and HTTP error handling for remote providers."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    async def _request_json(
        self, method: str, url: str, *, headers: dict[str, str] | None = None, **kwargs: Any
    ) -> dict[str, Any]:
        last_error: Exception | None = None
        for attempt in range(self.settings.llm_max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=self.settings.llm_timeout_seconds) as client:
                    response = await client.request(method, url, headers=headers, **kwargs)
                    response.raise_for_status()
                    payload = response.json()
                    if not isinstance(payload, dict):
                        raise LLMProviderError("Provider returned a non-object JSON response")
                    return payload
            except (httpx.HTTPError, ValueError, LLMProviderError) as exc:
                last_error = exc
                if attempt < self.settings.llm_max_retries:
                    await asyncio.sleep(0.25 * (2**attempt))
        raise LLMProviderError(f"{self.name} request failed") from last_error


class OpenAIProvider(_HTTPProvider):
    """OpenAI Chat Completions adapter isolated behind :class:`LLMProvider`."""

    name = "openai"

    async def generate(self, messages: list[LLMMessage]) -> str:
        if not self.settings.openai_api_key:
            raise LLMProviderError("CLOUDPROJ_OPENAI_API_KEY is not configured")
        payload = {
            "model": self.settings.openai_model,
            "messages": [message.model_dump() for message in messages],
            "temperature": 0,
        }
        result = await self._request_json(
            "POST",
            f"{self.settings.openai_base_url.rstrip('/')}/chat/completions",
            headers={"Authorization": f"Bearer {self.settings.openai_api_key.get_secret_value()}"},
            json=payload,
        )
        try:
            return result["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise LLMProviderError("Unexpected OpenAI response shape") from exc


class GeminiProvider(_HTTPProvider):
    """Google Gemini REST adapter isolated behind :class:`LLMProvider`."""

    name = "gemini"

    async def generate(self, messages: list[LLMMessage]) -> str:
        if not self.settings.gemini_api_key:
            raise LLMProviderError("CLOUDPROJ_GEMINI_API_KEY is not configured")
        contents = [
            {
                "role": "model" if message.role == "assistant" else "user",
                "parts": [{"text": message.content}],
            }
            for message in messages
            if message.role != "system"
        ]
        system_messages = [message.content for message in messages if message.role == "system"]
        payload: dict[str, Any] = {"contents": contents, "generationConfig": {"temperature": 0}}
        if system_messages:
            payload["systemInstruction"] = {"parts": [{"text": "\n".join(system_messages)}]}
        url = (
            f"{self.settings.gemini_base_url.rstrip('/')}/models/"
            f"{self.settings.gemini_model}:generateContent"
        )
        result = await self._request_json(
            "POST",
            url,
            params={"key": self.settings.gemini_api_key.get_secret_value()},
            json=payload,
        )
        try:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError, TypeError) as exc:
            raise LLMProviderError("Unexpected Gemini response shape") from exc


class OllamaProvider(_HTTPProvider):
    """Local Ollama REST adapter; no API key is required."""

    name = "ollama"

    async def generate(self, messages: list[LLMMessage]) -> str:
        payload = {
            "model": self.settings.ollama_model,
            "messages": [message.model_dump() for message in messages],
            "stream": False,
            "options": {"temperature": 0},
        }
        result = await self._request_json(
            "POST",
            f"{self.settings.ollama_base_url.rstrip('/')}/api/chat",
            json=payload,
        )
        try:
            return result["message"]["content"]
        except (KeyError, TypeError) as exc:
            raise LLMProviderError("Unexpected Ollama response shape") from exc


def build_llm_provider(provider: str | None = None, settings: Settings | None = None) -> LLMProvider:
    """Build the configured adapter without leaking provider logic into services."""

    settings = settings or get_settings()
    selected = (provider or settings.default_llm_provider).strip().lower()
    if selected == "stub":
        return StubLLMProvider()
    providers: dict[str, type[_HTTPProvider]] = {
        "openai": OpenAIProvider,
        "gemini": GeminiProvider,
        "ollama": OllamaProvider,
    }
    try:
        return providers[selected](settings)
    except KeyError as exc:
        supported = ", ".join(["stub", *sorted(providers)])
        raise ValueError(f"Unsupported LLM provider '{selected}'. Choose: {supported}") from exc
