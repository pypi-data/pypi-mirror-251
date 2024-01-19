import pwd
from os import getgid

from nwon_deployment.helper.running_on_gitlab_ci import running_on_gitlab_ci


def get_group_id(group_name: str = "gitlab-runner"):
    if running_on_gitlab_ci():
        try:
            return pwd.getpwnam(group_name).pw_gid
        except KeyError:
            pass

    return getgid()


__all__ = ["get_group_id"]
