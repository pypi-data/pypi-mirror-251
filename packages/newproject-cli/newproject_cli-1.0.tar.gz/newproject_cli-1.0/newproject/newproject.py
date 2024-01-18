#!/usr/bin/env python3

import errno
import json
import logging
import os
import subprocess
import sys
from pathlib import Path
from shutil import which
from typing import Final

import typer
import yaml
from rich.console import Console
from typing_extensions import Annotated

import newproject.error_codes
from newproject._version import __version__
from newproject.check import config_file_validator, dev_dir_check, projects_path_check, project_name_check
from newproject.utils import get_config_path, select_config_file
from newproject.error_logger import log_error

# rich
console = Console()

# Outputs
DONE: Final[str] = "✓ Done.\n"
PROJECT_STRUCTURE_GEN: Final[str] = "[dodger_blue1]Creating the project structure...[/dodger_blue1]"
HAPPY_CODING: Final[str] = "[gold1]⫸ Happy Coding![/gold1]"
CREATING_NEW_PROJECT: Final[str] = "[dodger_blue1]Creating your new project...[/dodger_blue1]\n"


class NewProject:
    def __init__(self):
        # Config file and JSON Schema
        self.YAML_CONFIG_FILE: Final[str] = select_config_file()
        self.JSON_SCHEMA_FILE: Final[str] = f"{get_config_path()}/schema/json_schema.json"

        # Loads YAML config file
        try:
            with open(self.YAML_CONFIG_FILE) as config_file:
                self.newproject_config = yaml.safe_load(config_file)
        except FileNotFoundError:
            log_error(error_code=newproject.error_codes.YAML_CONFIG_FILE_NOT_FOUND_ERROR)
            sys.exit(errno.ENOENT)

        # Loads JSON Schema file
        try:
            with open(self.JSON_SCHEMA_FILE) as json_schema_f:
                self.json_schema = json.load(json_schema_f)
        except FileNotFoundError:
            log_error(error_code=newproject.error_codes.JSON_SCHEMA_FILE_NOT_FOUND_ERROR)
            sys.exit(errno.ENOENT)

        # Default Development folder
        dev_dir = f"{Path.home()}/{self.newproject_config['development_dir_path']}"
        if dev_dir_check(dev_dir=dev_dir):
            self.DEV_DIR: Final[str] = f"{Path.home()}/{self.newproject_config['development_dir_path']}"
        else:
            sys.exit(errno.ENOENT)

        if config_file_validator(
                config_file=self.newproject_config, json_schema=self.json_schema
        ):
            # Project folder names
            self.PROJECTS_DIR_NAMES: Final[dict] = {
                "b9ash": self.newproject_config["bash"]["projects_dir_name"],
                "c_lang": self.newproject_config["c_lang"]["projects_dir_name"],
                "cpp": self.newproject_config["cpp"]["projects_dir_name"],
                "go": self.newproject_config["go"]["projects_dir_name"],
                "java": self.newproject_config["java"]["projects_dir_name"],
                "lua": self.newproject_config["lua"]["projects_dir_name"],
                "ocaml": self.newproject_config["ocaml"]["projects_dir_name"],
                "php": self.newproject_config["php"]["projects_dir_name"],
                "python": self.newproject_config["python"]["projects_dir_name"],
                "ruby": self.newproject_config["ruby"]["projects_dir_name"],
                "rust": self.newproject_config["rust"]["projects_dir_name"],
                "vlang": self.newproject_config["vlang"]["projects_dir_name"],
                "web": self.newproject_config["web"]["projects_dir_name"],
            }

    @staticmethod
    def open_in_ide(ide_command: str, project_dir: str) -> None:
        """
        Open the project in the specified IDE
        :param ide_command: (str) the console command to open the IDE
        :param project_dir: (str) the project directory to open in the IDE
        """
        if ide_command in ["code", "pycharm", "idea"] and which(f"{ide_command}") is not None:
            try:
                subprocess.run([f"{ide_command}", project_dir])
            except Exception as open_in_ide_error:
                logging.error(open_in_ide_error)
        elif ide_command:
            log_error(error_code=newproject.error_codes.IDE_NOT_FOUND_ERROR, ide_command=ide_command)

    def git_init_command(self, project_dir: str, content: str) -> None:
        """
        Initialize a local git repository
        :param project_dir: (str) project directory
        :param content: (str) the content of the .gitignore file
        """
        console.print(
            "[dodger_blue1]Initializing [underline]git[/underline] repository[/dodger_blue1]"
        )
        if which("git") is not None:
            try:
                subprocess.run(["git", "init", project_dir])

                # Creating .gitignore file
                try:
                    with open(f"{project_dir}/.gitignore", "w") as gitignore_f:
                        if content != "":
                            gitignore_f.write(content)
                        else:
                            gitignore_f.write(
                                self.newproject_config["default_gitignore_content"]
                            )

                        console.print("▶ [underline].gitignore[/underline] created.")

                        print(DONE)

                except Exception as gitignore_error:
                    log_error(error_code=newproject.error_codes.GITIGNORE_ERROR, gitignore_error=gitignore_error)

            except Exception as git_error:
                log_error(error_code=newproject.error_codes.GIT_ERROR, git_error=git_error)
        else:
            log_error(error_code=newproject.error_codes.GIT_NOT_INSTALLED)

    @staticmethod
    def create_and_write_file(new_project_dir: str, file_name: str, content: str) -> None:
        """
        Creates and writes a file
        :param new_project_dir: (str) the directory of the new project
        :param file_name: (str) file's name
        :param content: (str) content to write to file
        """
        # Creating the file structure
        console.print(PROJECT_STRUCTURE_GEN)
        try:
            with open(f"{new_project_dir}/{file_name}", "w") as project_file:
                project_file.write(content)
                console.print(f"▶ [underline]{file_name}[/underline] created.")
            print(DONE)
        except Exception as create_and_write_file_error:
            log_error(error_code=newproject.error_codes.CREATE_OR_WRITE_ERROR,
                      create_or_write_error=create_and_write_file_error,
                      not_writable_file=file_name
                      )

    @staticmethod
    def create_python_venv(new_project_path: str) -> None:
        """
        Create a python venv
        :param new_project_path: (str) path of the new python project
        """
        console.print(
            "[dodger_blue1]Generating the [underline]venv[/underline]...[/dodger_blue1]"
        )
        try:
            # MacOS and Linux
            if sys.platform.startswith("darwin") or sys.platform.startswith("linux"):
                with console.status("[dodger_blue1]Generating...[/dodger_blue1]", spinner="aesthetic"):
                    subprocess.run(["python3", "-m", "venv", f"{new_project_path}/venv"])
            # Windows
            elif sys.platform.startswith("win32"):
                with console.status("[dodger_blue1]Generating...[/dodger_blue1]", spinner="aesthetic"):
                    if which("virtualenv") is not None:
                        subprocess.run(["virtualenv", f"{new_project_path}/venv"])
                    else:
                        subprocess.run(["python3", "-m", "venv", f"{new_project_path}/venv"])
            print(DONE)
        except Exception as venv_exception:
            log_error(error_code=newproject.error_codes.PYTHON_VENV_ERROR, venv_error=venv_exception)

    @staticmethod
    def create_readme(new_project_dir, project_name):
        try:
            with open(f"{new_project_dir}/README.md", "w") as readme:
                readme.write(f"# {project_name}")
        except Exception as readme_error:
            log_error(error_code=newproject.error_codes.README_ERROR, readme_error=readme_error)

    def create_project(
            self,
            projects_dir_name: str,
            project_name: str,
            file_name: str,
            file_content: str,
            gitignore_content: str,
            ide: str = "",
    ):
        """
        Create a new project
        :param projects_dir_name: (str) the name of the specified programming language's directory
        :param project_name: (str) the name of the new project
        :param file_name: (str) the name of the file
        :param file_content: (str) content to write to file
        :param gitignore_content: (str) the content of the .gitignore file
        :param ide: (str) the name of the IDE where you want to open the new project
        """
        projects_folder_path = os.path.join(self.DEV_DIR, projects_dir_name)
        projects_path_check(projects_folder_to_check=projects_folder_path)

        # Creating the project folder
        new_project_dir = f"{projects_folder_path}/{project_name}"

        try:
            console.print(CREATING_NEW_PROJECT)

            os.mkdir(new_project_dir)

            if projects_dir_name == self.PROJECTS_DIR_NAMES["python"]:
                # Generating a python venv for the project
                self.create_python_venv(new_project_path=new_project_dir)

            # Creating the file structure
            self.create_and_write_file(
                new_project_dir=new_project_dir,
                file_name=file_name,
                content=file_content,
            )

            # Creating the README for the new project
            self.create_readme(new_project_dir=new_project_dir, project_name=project_name)

            # git init
            self.git_init_command(project_dir=new_project_dir, content=gitignore_content)

            # Open in IDE
            self.open_in_ide(ide_command=ide, project_dir=new_project_dir)

            console.print(HAPPY_CODING)

        except FileExistsError:
            log_error(error_code=newproject.error_codes.PROJECT_ALREADY_EXISTS_ERROR,
                      already_existent_project=new_project_dir)
            sys.exit(errno.EEXIST)

    def create_project_with_commands(
            self,
            projects_dir_name: str,
            project_name: str,
            ide: str = "",
    ):
        """
        Create a new project via dedicated commands.
        :param projects_dir_name: (str) the name of the specified programming language's directory
        :param project_name: (str) the name of the new project
        :param ide: (str) the name of the IDE where you want to open the new project
        """
        projects_path = os.path.join(self.DEV_DIR, projects_dir_name)

        projects_path_check(projects_folder_to_check=projects_path)
        # Creating the project folder
        new_project_dir = f"{projects_path}/{project_name}"

        try:
            if os.path.isdir(new_project_dir):
                raise FileExistsError(
                    errno.ENOENT, os.strerror(errno.ENOENT), new_project_dir
                )
            # Creating the project folder and file structure for the project
            console.print(CREATING_NEW_PROJECT)

            commands = []

            if projects_dir_name == self.PROJECTS_DIR_NAMES["rust"]:
                commands = ["cargo", "new", new_project_dir]
            elif projects_dir_name == self.PROJECTS_DIR_NAMES["ruby"]:
                commands = ["bundler", "gem", new_project_dir]
            elif projects_dir_name == self.PROJECTS_DIR_NAMES["ocaml"]:
                commands = ["dune", "init", "project", new_project_dir]
            elif projects_dir_name == self.PROJECTS_DIR_NAMES["vlang"]:
                commands = ["v", "new", new_project_dir]

            if which(commands[0]) is not None:
                try:
                    subprocess.run(commands)
                    print(DONE)

                    # Open in IDE
                    self.open_in_ide(ide_command=ide, project_dir=new_project_dir)

                    console.print(HAPPY_CODING)
                except Exception as command_exception:
                    log_error(error_code=newproject.error_codes.COMMAND_ERROR,
                              unsuccessful_command=commands[0],
                              command_error=command_exception)
            else:
                log_error(error_code=newproject.error_codes.COMMAND_NOT_FOUND_ERROR,
                          unsuccessful_command=commands[0])
                sys.exit(127)
        except FileExistsError:
            log_error(error_code=newproject.error_codes.PROJECT_ALREADY_EXISTS_ERROR,
                      already_existent_project=new_project_dir)
            sys.exit(errno.EEXIST)

    def create_web_project(
            self,
            projects_dir_name: str,
            project_name: str,
            html_file_content: str,
            css_file_content: str,
            javascript_file_content: str,
            gitignore_content: str,
            ide: str = "",
    ):
        """
        Create a basic new web project
        :param projects_dir_name: (str) the name of the specified programming language's directory
        :param project_name: (str) the name of the new project
        :param html_file_content: (str) the content of the html file
        :param css_file_content: (str) the content of the css file
        :param javascript_file_content: (str) the content of the javascript file
        :param gitignore_content: (str) the content of the .gitignore file
        :param ide: (str) the name of the IDE where you want to open the new project
        """

        projects_path = os.path.join(self.DEV_DIR, projects_dir_name)

        projects_path_check(projects_folder_to_check=projects_path)
        # Creating the project folder
        new_project_dir = f"{projects_path}/{project_name}"

        try:
            console.print(CREATING_NEW_PROJECT)

            os.mkdir(new_project_dir)
            os.mkdir(f"{new_project_dir}/styles")
            os.mkdir(f"{new_project_dir}/scripts")

            # Creating the file structure

            # Creating HTML file
            self.create_and_write_file(
                new_project_dir=new_project_dir,
                file_name="index.html",
                content=html_file_content,
            )
            # Creating CSS file
            self.create_and_write_file(
                new_project_dir=f"{new_project_dir}/styles",
                file_name="style.css",
                content=css_file_content,
            )
            # Creating Javascript file
            self.create_and_write_file(
                new_project_dir=f"{new_project_dir}/scripts",
                file_name="index.js",
                content=javascript_file_content,
            )

            # Creating the README for the new project
            self.create_readme(
                new_project_dir=new_project_dir, project_name=project_name
            )

            # git init
            self.git_init_command(
                project_dir=new_project_dir, content=gitignore_content
            )

            # Open in IDE
            self.open_in_ide(ide_command=ide, project_dir=new_project_dir)

            console.print(HAPPY_CODING)

        except FileExistsError:
            log_error(error_code=newproject.error_codes.PROJECT_ALREADY_EXISTS_ERROR,
                      already_existent_project=new_project_dir)
            sys.exit(errno.EEXIST)

    def handle(
            self,
            bash: Annotated[str, typer.Option(help="create a bash project")] = "",
            clang: Annotated[str, typer.Option(help="create a c project")] = "",
            cpp: Annotated[str, typer.Option(help="create a cpp project")] = "",
            go: Annotated[str, typer.Option(help="create a go project")] = "",
            java: Annotated[str, typer.Option(help="create a java project")] = "",
            lua: Annotated[str, typer.Option(help="create a lua project")] = "",
            ocaml: Annotated[str, typer.Option(help="create an ocaml project")] = "",
            php: Annotated[str, typer.Option(help="create a php project")] = "",
            python: Annotated[str, typer.Option(help="create a python project")] = "",
            ruby: Annotated[str, typer.Option(help="create a ruby project")] = "",
            rust: Annotated[str, typer.Option(help="create a rust project")] = "",
            vlang: Annotated[str, typer.Option(help="create a vlang project")] = "",
            web: Annotated[str, typer.Option(help="create a basic web project")] = "",
            code: Annotated[bool, typer.Option(help="open the project in VS Code")] = False,
            idea: Annotated[bool, typer.Option(help="open the project in Intellij IDEA")] = False,
            pycharm: Annotated[bool, typer.Option(help="open the project in PyCharm")] = False,
            version: Annotated[bool, typer.Option(help="show the newproject-cli version")] = False
    ):
        """
        Create a new project via terminal

        Coded with <3 by utox39
        """

        if version:
            version_callback(value=True)

        ide_name = ""
        if code:
            ide_name = "code"
        elif pycharm:
            ide_name = "pycharm"
        elif idea:
            ide_name = "idea"

        project_mapping = {
            python: (
                self.create_project,
                self.PROJECTS_DIR_NAMES["python"],
                python,
                f"{python}.py",
                self.newproject_config["python"]["file_content"],
                self.newproject_config["python"]["gitignore_content"],
                ide_name,
            ),
            java: (
                self.create_project,
                self.PROJECTS_DIR_NAMES["java"],
                java,
                "Main.java",
                self.newproject_config["java"]["file_content"],
                self.newproject_config["java"]["gitignore_content"],
                ide_name,
            ),
            go: (
                self.create_project,
                self.PROJECTS_DIR_NAMES["go"],
                go,
                "main.go",
                self.newproject_config["go"]["file_content"],
                self.newproject_config["go"]["gitignore_content"],
                ide_name,
            ),
            bash: (
                self.create_project,
                self.PROJECTS_DIR_NAMES["bash"],
                bash,
                f"{bash}.sh",
                self.newproject_config["bash"]["file_content"],
                self.newproject_config["bash"]["gitignore_content"],
                ide_name,
            ),
            cpp: (
                self.create_project,
                self.PROJECTS_DIR_NAMES["cpp"],
                cpp,
                "main.cpp",
                self.newproject_config["cpp"]["file_content"],
                self.newproject_config["cpp"]["gitignore_content"],
                ide_name,
            ),
            clang: (
                self.create_project,
                self.PROJECTS_DIR_NAMES["c_lang"],
                clang,
                "main.c",
                self.newproject_config["c_lang"]["file_content"],
                self.newproject_config["c_lang"]["gitignore_content"],
                ide_name,
            ),
            php: (
                self.create_project,
                self.PROJECTS_DIR_NAMES["php"],
                php,
                "index.php",
                self.newproject_config["php"]["file_content"],
                self.newproject_config["php"]["gitignore_content"],
                ide_name,
            ),
            lua: (
                self.create_project,
                self.PROJECTS_DIR_NAMES["lua"],
                lua,
                "main.lua",
                self.newproject_config["lua"]["file_content"],
                self.newproject_config["lua"]["gitignore_content"],
                ide_name,
            ),
            rust: (
                self.create_project_with_commands,
                self.PROJECTS_DIR_NAMES["rust"],
                rust,
                ide_name,
            ),
            ruby: (
                self.create_project_with_commands,
                self.PROJECTS_DIR_NAMES["ruby"],
                ruby,
                ide_name,
            ),
            ocaml: (
                self.create_project_with_commands,
                self.PROJECTS_DIR_NAMES["ocaml"],
                ocaml,
                ide_name,
            ),
            vlang: (
                self.create_project_with_commands,
                self.PROJECTS_DIR_NAMES["vlang"],
                vlang,
                ide_name,
            ),
            web: (
                self.create_web_project,
                self.PROJECTS_DIR_NAMES["web"],
                web,
                self.newproject_config["web"]["html_file_content"],
                self.newproject_config["web"]["css_file_content"],
                self.newproject_config["web"]["javascript_file_content"],
                self.newproject_config["web"]["gitignore_content"],
                ide_name,
            ),
        }

        for flag, func_and_proj_info in project_mapping.items():
            if flag:
                create_func, *args = func_and_proj_info
                # Checks if the project_name doesn't contain: spaces, &&, ||
                project_name_check(flag)

                create_func(*args)
                break
        else:
            console.print("[bold red]No option provided[/bold red]")


def version_callback(value: bool):
    if value:
        print(f"newproject-cli version: {__version__}")
        raise typer.Exit()


def main():
    typer.run(NewProject().handle)


if __name__ == "__main__":
    main()
