from enum import Enum
from os.path import exists

from mergedeep import merge
from pydantic import BaseModel

from nwon_deployment.environment.current_deployment_environment import (
    current_deployment_environment,
)
from nwon_deployment.exceptions.setting_file_do_not_exist import SettingFileDoNotExist
from nwon_deployment.setting_files.create_setting_override_file import (
    create_setting_override_file,
)
from nwon_deployment.setting_files.load_settings_from_file import (
    load_settings_from_file,
)
from nwon_deployment.setting_files.setting_file_paths import (
    path_base_setting_file,
    path_settings_override_file,
)
from nwon_deployment.settings import get_deployment_package_settings


def get_application_settings() -> BaseModel:
    """
    Get deployment settings.

    Settings are defined via a settings.toml file in the directory of the deployment
    environment. On top all settings can be overridden using a settings.override.toml
    file in the same directory.
    """

    environment = current_deployment_environment()
    return get_application_settings_for_environment(environment)


def get_application_settings_for_environment(environment: Enum) -> BaseModel:
    """
    Get deployment settings for a specific environment.

    Settings are defined via a settings.toml file in the directory of the deployment
    environment. On top all settings can be overridden using a settings.override.toml
    file in the same directory.
    """

    setting_file = path_base_setting_file(environment)
    setting_override_file = path_settings_override_file(environment)

    if not exists(setting_override_file):
        create_setting_override_file(environment)

    if not exists(setting_file):
        raise SettingFileDoNotExist(
            f"Base setting file for environment {str(environment)} "
            f"does not exist in {setting_file}"
        )

    settings = load_settings_from_file(setting_file)

    if exists(setting_override_file):
        user_settings = load_settings_from_file(setting_override_file)
        settings = merge(settings, user_settings)

    deployment_package_settings = get_deployment_package_settings()
    return deployment_package_settings.application_settings.settings.model_validate(
        settings
    )
