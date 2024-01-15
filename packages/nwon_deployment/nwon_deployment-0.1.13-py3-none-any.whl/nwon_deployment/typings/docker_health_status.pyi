from enum import Enum

class DockerHealthStatus(Enum):
    Starting: str
    Healthy: str
    Unhealthy: str
