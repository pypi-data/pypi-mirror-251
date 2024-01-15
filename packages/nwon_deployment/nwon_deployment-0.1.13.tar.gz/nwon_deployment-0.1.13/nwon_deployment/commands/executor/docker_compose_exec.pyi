from nwon_deployment.typings import DockerService as DockerService
from typing import List

def docker_compose_exec(options: List[str], service: DockerService, command: str, interactive: bool = ...): ...
