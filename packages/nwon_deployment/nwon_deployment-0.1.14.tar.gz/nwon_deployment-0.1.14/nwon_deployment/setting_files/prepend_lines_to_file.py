from nwon_deployment.helper.dump_application_settings_optional_schema import (
    optional_json_schema_file_name,
)
from nwon_deployment.settings import get_deployment_package_settings


def prepend_lines_to_file(file_path: str):
    settings = get_deployment_package_settings()

    lines = [
        f"#:schema {optional_json_schema_file_name()}",
        "",
    ] + settings.application_settings.lines_to_prepend_to_settings_override

    for line in lines[::-1]:
        with open(file_path, "r+", encoding="utf-8") as file:
            content = file.read()
            file.seek(0, 0)
            file.write(line.rstrip("\r\n") + "\n" + content)
