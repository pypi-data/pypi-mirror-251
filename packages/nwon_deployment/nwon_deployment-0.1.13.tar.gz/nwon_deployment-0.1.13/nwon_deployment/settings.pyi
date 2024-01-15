from enum import Enum
from nwon_deployment.environment_variables.env_variable_map import EnvVariableMap as EnvVariableMap
from nwon_deployment.typings.deployment_base_model import DeploymentBaseModel as DeploymentBaseModel
from pydantic.generics import GenericModel
from typing import Callable, Dict, Generic, List, Optional, Set, TypeVar, Union

DockerService = TypeVar('DockerService', bound=Enum)

class DeploymentSettingsGitlab(DeploymentBaseModel):
    use_gitlab_container_registry: bool
    user_name: Optional[str]
    password: Optional[str]
    api_token: Optional[str]
    gitlab_registry_url: Optional[str]

class DeploymentSettings(GenericModel, Generic[DockerService]):
    stack_name: str
    container_name: Callable[[str, int], str]
    user_for_container: Dict[DockerService, str]
    default_command_for_container: Dict[DockerService, str]
    gitlab: Optional[DeploymentSettingsGitlab]
    env_variable_map: EnvVariableMap
    compose_files: Callable[..., Union[Set[str], List[str]]]

def set_deployment_settings(settings: DeploymentSettings[Enum]) -> DeploymentSettings[Enum]: ...
def get_deployment_settings() -> DeploymentSettings[Enum]: ...
