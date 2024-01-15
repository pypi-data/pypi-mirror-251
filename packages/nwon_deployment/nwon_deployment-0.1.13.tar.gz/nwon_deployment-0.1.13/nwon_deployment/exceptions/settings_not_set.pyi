from nwon_deployment.exceptions.deployment_exception import DeploymentException as DeploymentException

class DeploymentSettingsNotSet(DeploymentException):
    message: str
