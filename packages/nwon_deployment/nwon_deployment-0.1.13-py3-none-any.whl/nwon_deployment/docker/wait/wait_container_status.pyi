from docker.models.containers import Container as Container
from nwon_deployment.typings.container_status import ContainerStatus as ContainerStatus
from typing import List, Optional

def wait_container_status(container_name: str, seconds_to_wait: int = ..., status_to_wait: Optional[List[ContainerStatus]] = ...) -> Container: ...
