"""Cloud/deployment provider contracts."""

from abc import ABC, abstractmethod

from pydantic import BaseModel


class DeploymentRequest(BaseModel):
    project_name: str
    artifact_path: str
    environment: str = "development"


class DeploymentResult(BaseModel):
    provider: str
    status: str
    endpoint: str | None = None
    details: dict[str, object] = {}


class CloudProvider(ABC):
    """Provider-neutral deployment interface."""

    name: str

    @abstractmethod
    async def deploy(self, request: DeploymentRequest) -> DeploymentResult:
        raise NotImplementedError


class DockerCloudProvider(CloudProvider):
    """Local container target used before cloud adapters are introduced."""

    name = "docker"

    async def deploy(self, request: DeploymentRequest) -> DeploymentResult:
        return DeploymentResult(
            provider=self.name,
            status="planned",
            details={"project": request.project_name, "artifact": request.artifact_path},
        )
