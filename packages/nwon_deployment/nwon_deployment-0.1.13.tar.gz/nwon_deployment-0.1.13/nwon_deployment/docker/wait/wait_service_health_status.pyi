from docker.models.containers import Container as Container
from enum import Enum
from nwon_deployment.typings import DockerHealthStatus as DockerHealthStatus
from typing import List, Optional, TypeVar

DockerService = TypeVar('DockerService', bound=Enum)

def wait_service_health_status(service: DockerService, status_to_wait_for: Optional[List[DockerHealthStatus]] = ..., seconds_to_wait: int = ..., container_index: int = ...) -> Container: ...
