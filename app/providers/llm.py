"""LLM provider contract and deterministic local implementation."""

from abc import ABC, abstractmethod

from pydantic import BaseModel


class LLMMessage(BaseModel):
    role: str
    content: str


class LLMProvider(ABC):
    """Provider-neutral interface for language models."""

    @abstractmethod
    async def generate(self, messages: list[LLMMessage]) -> str:
        raise NotImplementedError


class StubLLMProvider(LLMProvider):
    """Deterministic provider used for local development and tests."""

    async def generate(self, messages: list[LLMMessage]) -> str:
        user_messages = [message.content for message in messages if message.role == "user"]
        return user_messages[-1] if user_messages else "No user requirement supplied."
