from enum import Enum
from typing import TypeVar

DockerService = TypeVar('DockerService', bound=Enum)

def run_on_container(service: DockerService, command: str): ...
