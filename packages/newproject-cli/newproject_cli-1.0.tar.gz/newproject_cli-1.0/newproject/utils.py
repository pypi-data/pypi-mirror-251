#!/usr/bin/env python3

import os
import site
import sys

from pathlib import Path


def get_config_path() -> str:
    # Gets the site-packages path
    site_packages = ""
    if sys.platform.startswith("darwin"):
        site_packages = site.getsitepackages()[0]
    elif sys.platform.startswith("linux"):
        if os.path.exists(site.getusersitepackages()):
            site_packages = site.getusersitepackages()
    elif sys.platform.startswith("win32"):
        site_packages = site.getsitepackages()[1]

    newproject_cli_config_files_path = os.path.join(site_packages, "newproject/config")

    return newproject_cli_config_files_path


def select_config_file() -> str:
    """
    Checks the presence of the configuration file in .config and if it exists it returns its path,
    otherwise it returns the path of the one located in site_packages.
    :return: (str) the config file path
    """
    dot_config_yaml_file = f"{Path.home()}/.config/newproject/newproject_config.yaml"
    site_packages_config_file = f"{get_config_path()}/newproject_config.yaml"

    if os.path.exists(dot_config_yaml_file):
        return dot_config_yaml_file
    else:
        return site_packages_config_file
