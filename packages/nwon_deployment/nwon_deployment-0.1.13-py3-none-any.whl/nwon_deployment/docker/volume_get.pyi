from docker.models.volumes import Volume as Volume
from typing import Optional

def volume_get(volume_name: str) -> Optional[Volume]: ...
