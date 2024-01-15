from nwon_deployment.exceptions.deployment_exception import DeploymentException as DeploymentException

class ContainerNotAvailable(DeploymentException):
    message: str
    def __init__(self, container_name: str, seconds_to_wait: int, *args: object) -> None: ...
