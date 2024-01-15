from nwon_deployment.settings import get_deployment_settings
from nwon_deployment.typings import DockerService


def container_name_for_service(service: DockerService, index: int = 1):
    return get_deployment_settings().container_name(service.value, index)


__all__ = ["container_name_for_service"]
