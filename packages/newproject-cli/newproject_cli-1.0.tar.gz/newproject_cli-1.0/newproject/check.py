#!/usr/bin/env python3

import errno
import os
import sys

from typing import Final

import jsonschema

from rich.console import Console

import newproject.error_codes
from newproject.error_logger import log_error

EXIT_FAILURE: Final[int] = 1  # lol C

# rich config
console = Console()


def config_file_validator(config_file, json_schema) -> bool | None:
    try:
        jsonschema.validate(instance=config_file, schema=json_schema)
        return True
    except jsonschema.ValidationError as validation_error:
        if validation_error.relative_path:
            print(f"{validation_error.relative_path[0]}:")

            message_len = len(validation_error.relative_path) - 1
            if validation_error.validator == "required":
                print(f"  {validation_error.message[1:-24]} (missing)\n")
            else:
                print(f"  {validation_error.relative_path[message_len]}:(type error)\n")

        if validation_error.context:
            print(validation_error.context)
        if validation_error.cause:
            print(validation_error.cause)

        # print(f"newproject: yaml config file error: {validation_error.message}")
        log_error(error_code=newproject.error_codes.YAML_CONFIG_FILE_GENERIC_ERROR, yaml_error=validation_error.message)
        sys.exit(EXIT_FAILURE)


def dev_dir_check(dev_dir: str) -> None | bool:
    """
    Check if the development folder exists
    :return bool: True if the development folder exists
    """
    if not os.path.isdir(dev_dir):
        log_error(error_code=newproject.error_codes.DEVELOPMENT_DIR_NOT_FOUND_ERROR, folder=dev_dir)
        # sys.exit(errno.ENOENT)
    else:
        return True


def projects_path_check(projects_folder_to_check: str) -> None:
    """
    Check if the specified programming language project folder exists
    :param projects_folder_to_check: (str) name of the programming language projects folder
    """
    if not os.path.isdir(projects_folder_to_check):
        log_error(error_code=newproject.error_codes.PROJECTS_FOLDER_NOT_FOUND_ERROR, folder=projects_folder_to_check)
        sys.exit(errno.ENOENT)


def project_name_check(project_name: str) -> None:
    """
    Checks if the project name contains a space
    :param project_name: (str) the name of the project
    """
    if " " in project_name:
        log_error(error_code=newproject.error_codes.INVALID_PROJECT_NAME, invalid_character="spaces")
        sys.exit(EXIT_FAILURE)
    if "&&" in project_name:
        log_error(error_code=newproject.error_codes.INVALID_PROJECT_NAME, invalid_character="&&")
        sys.exit(EXIT_FAILURE)
    if "||" in project_name:
        log_error(error_code=newproject.error_codes.INVALID_PROJECT_NAME, invalid_character="||")
        sys.exit(EXIT_FAILURE)
