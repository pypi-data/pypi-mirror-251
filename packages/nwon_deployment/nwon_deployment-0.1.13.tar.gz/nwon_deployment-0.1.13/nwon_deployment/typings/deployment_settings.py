from typing import Callable, Dict, Generic, List, Optional, Set, Union

from pydantic import BaseModel

from nwon_deployment.typings.deployment_base_model import DeploymentBaseModel
from nwon_deployment.typings.docker_service import DockerService
from nwon_deployment.typings.env_variable_map import EnvVariableMap


class DeploymentSettingsGitlab(DeploymentBaseModel):
    use_gitlab_container_registry: bool
    user_name: Optional[str] = None
    password: Optional[str] = None
    api_token: Optional[str] = None
    gitlab_registry_url: Optional[str] = None


class DeploymentSettings(BaseModel, Generic[DockerService]):
    stack_name: str
    container_name: Callable[[str, int], str]
    user_for_container: Dict[DockerService, str]
    default_command_for_container: Dict[DockerService, str]
    gitlab: Optional[DeploymentSettingsGitlab] = None
    env_variable_map: EnvVariableMap
    compose_files: Callable[..., Union[Set[str], List[str]]]


__all__ = ["DeploymentSettingsGitlab", "DeploymentSettings"]
