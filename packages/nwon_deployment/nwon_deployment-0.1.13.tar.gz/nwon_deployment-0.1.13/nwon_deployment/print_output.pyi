from enum import Enum
from nwon_baseline.typings import TerminalColors
from nwon_deployment.typings.deployment_base_model import DeploymentBaseModel as DeploymentBaseModel
from typing import Dict, Optional

class OutputType(Enum):
    Docker: str
    Debug: str
    Information: str
    Command: str

class DeploymentPrintSetting(DeploymentBaseModel):
    debug: bool
    command: bool
    docker: bool
    information: bool

COLOR_MAP: Dict[OutputType, TerminalColors]

def print_output(text: str, output: OutputType = ..., color: Optional[TerminalColors] = ..., print_settings: Optional[DeploymentPrintSetting] = ...): ...
