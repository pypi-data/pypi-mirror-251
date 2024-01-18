#!/usr/bin/env python3

import logging

from rich.console import Console

import newproject.error_codes
from newproject.utils import select_config_file

# rich config
console = Console()

# Logging config
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def log_error(error_code: int,
              folder: str = "",
              invalid_character: str = "",
              yaml_error: str = "",
              ide_command: str = "",
              gitignore_error: Exception = None,
              git_error: Exception = None,
              create_or_write_error: Exception = None,
              not_writable_file: str = "",
              venv_error: Exception = None,
              readme_error: Exception = None,
              already_existent_project: str = "",
              unsuccessful_command: str = "",
              command_error: Exception = None
              ) -> None:
    match error_code:
        case newproject.error_codes.DEVELOPMENT_DIR_NOT_FOUND_ERROR | \
             newproject.error_codes.PROJECTS_FOLDER_NOT_FOUND_ERROR:
            console.print(f"newproject: error: [red3]{folder}[/red3] does not exist.")
            console.print(
                f"Check the YAML file: [dark_orange3][underline]{select_config_file()}[/underline][/dark_orange3]"
            )
        case newproject.error_codes.INVALID_PROJECT_NAME:
            console.print(
                f"newproject: error: invalid project name. Invalid character: [cyan2]{invalid_character}[/cyan2]"
            )
        case newproject.error_codes.YAML_CONFIG_FILE_NOT_FOUND_ERROR:
            console.print("newproject: error: yaml config file not found.")
        case newproject.error_codes.JSON_SCHEMA_FILE_NOT_FOUND_ERROR:
            console.print("newproject: error: json schema file not found.")
        case newproject.error_codes.YAML_CONFIG_FILE_GENERIC_ERROR:
            console.print(f"newproject: error: yaml config file error: [red1]{yaml_error}[/red1]")
        case newproject.error_codes.IDE_NOT_FOUND_ERROR:
            console.print(f"newproject: error: [dodger_blue1]{ide_command}[/dodger_blue1]: ide command not found.")
        case newproject.error_codes.GITIGNORE_ERROR:
            logging.error(gitignore_error)
            console.print("newproject: error: can't create .gitignore file.")
        case newproject.error_codes.GIT_ERROR:
            logging.error(git_error)
            console.print("newproject: error: can't initialize git repository.")
        case newproject.error_codes.GIT_NOT_INSTALLED:
            console.print("newproject: error: git is not installed.")
        case newproject.error_codes.CREATE_OR_WRITE_ERROR:
            logging.error(create_or_write_error)
            console.print(f"newproject: error: can't create or write [red3]{not_writable_file}[/red3]")
        case newproject.error_codes.PYTHON_VENV_ERROR:
            logging.error(venv_error)
            console.print("newproject: error: can't create python venv.")
        case newproject.error_codes.README_ERROR:
            logging.error(readme_error)
            console.print("newproject: error: can't create README.md file.")
        case newproject.error_codes.PROJECT_ALREADY_EXISTS_ERROR:
            console.print(
                f"newproject: error: [underline red3]{already_existent_project}[/underline red3] already exists."
            )
            console.print("[red3]𝙓 Could not create the project[/red3]")
        case newproject.error_codes.COMMAND_ERROR:
            console.print(f"newproject: error: {unsuccessful_command} generated an error.")
            console.print("[red3]𝙓 Could not create the project[/red3]")
            logging.error(command_error)
        case newproject.error_codes.COMMAND_NOT_FOUND_ERROR:
            console.print(f"newproject: error: [dodger_blue1]{unsuccessful_command}[/dodger_blue1]: command not found.")
