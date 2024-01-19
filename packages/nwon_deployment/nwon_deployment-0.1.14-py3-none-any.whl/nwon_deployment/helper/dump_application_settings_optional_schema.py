from os import path

from nwon_deployment.settings import get_deployment_package_settings


def dump_optional_schema_if_not_exists():
    if not path.exists(optional_json_schema_file_name()):
        dump_application_settings_optional_schema()


def optional_json_schema_file_name():
    settings = get_deployment_package_settings()
    return path.join(
        settings.paths.deployment_scripts_base,
        settings.application_settings.optional_json_schema_file_name,
    )


def dump_application_settings_optional_schema():
    settings = get_deployment_package_settings()
    schema = settings.application_settings.settings.model_json_schema()
    __set_required_to_false(schema)

    with open(optional_json_schema_file_name(), "w+", encoding="utf-8") as file:
        file.write(str(schema))


def __set_required_to_false(schema):
    if isinstance(schema, dict):
        for k, value in schema.items():
            if k == "required":
                schema[k] = False
            elif isinstance(value, dict):
                __set_required_to_false(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        __set_required_to_false(item)


__ALL__ = [
    "dump_application_settings_optional_schema",
    "optional_json_schema_file_name",
    "dump_optional_schema_if_not_exists",
]
