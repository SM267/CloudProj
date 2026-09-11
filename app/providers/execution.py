"""Generated-code execution abstraction."""

from abc import ABC, abstractmethod

from pydantic import BaseModel


class ExecutionRequest(BaseModel):
    artifact_path: str
    command: list[str]
    timeout_seconds: int = 60


class ExecutionResult(BaseModel):
    exit_code: int
    stdout: str
    stderr: str


class ExecutionProvider(ABC):
    @abstractmethod
    async def execute(self, request: ExecutionRequest) -> ExecutionResult:
        raise NotImplementedError
