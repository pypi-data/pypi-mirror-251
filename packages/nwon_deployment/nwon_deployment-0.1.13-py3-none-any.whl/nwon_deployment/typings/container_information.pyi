from docker.models.containers import Container as Container
from nwon_deployment.typings.container_status import ContainerStatus as ContainerStatus
from nwon_deployment.typings.deployment_base_model import DeploymentBaseModel as DeploymentBaseModel
from nwon_deployment.typings.docker_health_status import DockerHealthStatus as DockerHealthStatus
from typing import Optional

class ContainerInformation(DeploymentBaseModel):
    container: Container
    index: int
    health: Optional[DockerHealthStatus]
    status: ContainerStatus
    name: str
    class Config:
        arbitrary_types_allowed: bool
