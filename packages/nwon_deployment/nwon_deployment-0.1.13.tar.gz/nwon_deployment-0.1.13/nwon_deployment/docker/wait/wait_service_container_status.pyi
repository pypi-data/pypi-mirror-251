from docker.models.containers import Container as Container
from nwon_deployment.typings import ContainerStatus as ContainerStatus, DockerService as DockerService
from typing import List, Optional

def wait_service_container_status(service: DockerService, seconds_to_wait: int = ..., container_index: int = ..., status_to_wait: Optional[List[ContainerStatus]] = ...) -> Container: ...
