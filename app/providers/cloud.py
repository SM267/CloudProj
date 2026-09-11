"""Provider-neutral deployment contracts.

Concrete cloud integrations should implement :class:`CloudProvider`; the local
Docker adapter deliberately reports a plan rather than executing a deployment.
"""

from abc import ABC, abstractmethod

from pydantic import BaseModel, Field


class DeploymentRequest(BaseModel):
    """Inputs required by a deployment provider."""

    project_name: str = Field(min_length=1, max_length=100)
    artifact_path: str = Field(min_length=1, max_length=4096)
    environment: str = Field(default="development", min_length=1, max_length=50)


class DeploymentResult(BaseModel):
    """Provider-independent deployment outcome."""

    provider: str
    status: str
    endpoint: str | None = None
    details: dict[str, object] = Field(default_factory=dict)


class CloudProvider(ABC):
    """Provider-neutral deployment interface."""

    name: str

    @abstractmethod
    async def deploy(self, request: DeploymentRequest) -> DeploymentResult:
        """Deploy or plan deployment for an artifact."""
        raise NotImplementedError


class DockerCloudProvider(CloudProvider):
    """Safe local target used until concrete cloud adapters are added."""

    name = "docker"

    async def deploy(self, request: DeploymentRequest) -> DeploymentResult:
        """Return a non-destructive deployment plan."""

        return DeploymentResult(
            provider=self.name,
            status="planned",
            details={"project": request.project_name, "artifact": request.artifact_path},
        )
