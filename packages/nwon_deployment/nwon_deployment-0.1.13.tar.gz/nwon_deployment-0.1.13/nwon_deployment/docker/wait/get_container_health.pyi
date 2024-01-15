from docker.models.containers import Container as Container
from nwon_deployment.typings import DockerHealthStatus as DockerHealthStatus
from typing import Optional

def get_container_health(container: Container) -> Optional[DockerHealthStatus]: ...
