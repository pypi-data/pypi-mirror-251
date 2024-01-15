from nwon_deployment.exceptions.deployment_exception import DeploymentException as DeploymentException
from nwon_deployment.typings.docker_service import DockerService as DockerService

class ContainerForServiceNotAvailable(DeploymentException):
    message: str
    def __init__(self, service: DockerService, *args: object) -> None: ...
