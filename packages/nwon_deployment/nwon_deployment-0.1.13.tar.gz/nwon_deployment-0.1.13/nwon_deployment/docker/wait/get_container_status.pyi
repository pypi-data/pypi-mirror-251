from docker.models.containers import Container as Container
from nwon_deployment.typings import ContainerStatus as ContainerStatus

def get_container_status(container: Container) -> ContainerStatus: ...
