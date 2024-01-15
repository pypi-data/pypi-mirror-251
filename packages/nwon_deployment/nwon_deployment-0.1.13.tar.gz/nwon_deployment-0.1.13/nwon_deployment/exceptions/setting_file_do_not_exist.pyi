from nwon_deployment.exceptions.deployment_exception import DeploymentException as DeploymentException

class SettingFileDoNotExist(DeploymentException):
    message: str
