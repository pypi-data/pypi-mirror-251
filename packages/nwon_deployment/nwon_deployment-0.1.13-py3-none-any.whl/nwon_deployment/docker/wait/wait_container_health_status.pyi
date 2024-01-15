from docker.models.containers import Container as Container
from nwon_deployment.typings import DockerHealthStatus as DockerHealthStatus
from typing import List, Optional

def wait_container_health_status(container: Container, status_to_wait_for: Optional[List[DockerHealthStatus]] = ..., seconds_to_wait: int = ...): ...
