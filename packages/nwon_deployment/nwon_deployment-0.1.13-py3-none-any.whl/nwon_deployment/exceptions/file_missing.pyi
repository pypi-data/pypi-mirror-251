from nwon_deployment.exceptions.deployment_exception import DeploymentException as DeploymentException

class FileMissing(DeploymentException):
    message: str
    def __init__(self, path: str, *args: object) -> None: ...
