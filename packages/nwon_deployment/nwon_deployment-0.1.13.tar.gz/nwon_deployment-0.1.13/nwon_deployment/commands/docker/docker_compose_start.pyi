from nwon_deployment.typings import DockerService as DockerService
from typing import List, Optional

def docker_compose_start(service: Optional[DockerService] = ..., additional_options: Optional[List[str]] = ..., wait_for_healthy: bool = ...): ...
