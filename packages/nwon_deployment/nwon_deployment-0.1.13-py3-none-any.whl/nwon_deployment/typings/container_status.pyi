from enum import Enum

class ContainerStatus(Enum):
    Created: str
    Restarting: str
    Running: str
    Paused: str
    Exited: str
