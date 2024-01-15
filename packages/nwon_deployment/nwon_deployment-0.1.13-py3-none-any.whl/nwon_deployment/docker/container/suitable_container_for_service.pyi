from nwon_deployment.typings import ContainerInformation as ContainerInformation, DockerService as DockerService
from typing import Optional

def suitable_container_for_service(service: DockerService) -> Optional[ContainerInformation]: ...
