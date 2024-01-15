from nwon_deployment.typings.deployment_base_model import DeploymentBaseModel as DeploymentBaseModel
from nwon_deployment.typings.docker_service import DockerService as DockerService
from nwon_deployment.typings.env_variable_map import EnvVariableMap as EnvVariableMap
from pydantic import BaseModel
from typing import Callable, Dict, Generic, List, Optional, Set, Union

class DeploymentSettingsGitlab(DeploymentBaseModel):
    use_gitlab_container_registry: bool
    user_name: Optional[str]
    password: Optional[str]
    api_token: Optional[str]
    gitlab_registry_url: Optional[str]

class DeploymentSettings(BaseModel, Generic[DockerService]):
    stack_name: str
    container_name: Callable[[str, int], str]
    user_for_container: Dict[DockerService, str]
    default_command_for_container: Dict[DockerService, str]
    gitlab: Optional[DeploymentSettingsGitlab]
    env_variable_map: EnvVariableMap
    compose_files: Callable[..., Union[Set[str], List[str]]]
