from nwon_deployment.typings import DockerService as DockerService, DockerServiceActionMap as DockerServiceActionMap
from typing import Optional

def post_start_actions(service: DockerService, action_map: Optional[DockerServiceActionMap[DockerService]] = ...): ...
