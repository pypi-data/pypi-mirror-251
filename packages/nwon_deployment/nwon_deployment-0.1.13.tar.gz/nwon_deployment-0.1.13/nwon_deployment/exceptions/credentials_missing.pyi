from nwon_deployment.exceptions.deployment_exception import DeploymentException as DeploymentException

class CredentialsMissing(DeploymentException):
    message: str
