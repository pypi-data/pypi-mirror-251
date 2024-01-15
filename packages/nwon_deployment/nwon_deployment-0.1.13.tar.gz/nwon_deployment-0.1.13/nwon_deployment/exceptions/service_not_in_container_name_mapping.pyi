from enum import Enum
from nwon_deployment.exceptions.deployment_exception import DeploymentException as DeploymentException

class ServiceNotInContainerNameMapping(DeploymentException):
    message: str
    def __init__(self, service: Enum, *args: object) -> None: ...
