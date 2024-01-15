from enum import Enum

class DeploymentEnvironment(Enum):
    Review: str
    Development: str
    Testing: str
    Staging: str
    Production: str
