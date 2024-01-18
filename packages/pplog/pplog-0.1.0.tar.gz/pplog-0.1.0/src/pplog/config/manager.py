""" Configuration Singleton to live throughout the project's execution """


import os
from copy import deepcopy
from pathlib import Path, PosixPath
from typing import List, Union

from omegaconf import DictConfig, ListConfig, OmegaConf


#  pylint:disable=fixme, attribute-defined-outside-init
class ConfigurationParser:
    """.yaml configuration parser"""

    _CONF_FILE_PATTERN = "ppconf"
    _instance = None

    def __new__(cls, *args, **kwargs):
        """Ensure only one instance"""
        if not cls._instance:
            cls._instance = super(ConfigurationParser, cls).__new__(
                cls, *args, **kwargs
            )
            cls._instance._config = None
        return cls._instance

    def get_ppconfig(self):
        """Returns pplog's configuration parse from .yaml files"""
        if self._config is None:
            raise ValueError("Configuration not loaded. Call load_ppconfig() first.")
        return deepcopy(self._config)

    def load_ppconfig(self, config_folder: PosixPath) -> None:
        """Loads pplog configuration from a specified folder pathlib.PosixPath object

        Args:
            config_folder (PosixPath): pplog .yml, .yaml, .json config files location

        Raises:
            FileNotFoundError: No configuration files found or incorrect path provided

        Returns:
            Union[ListConfig, DictConfig]: OmegaConf object - loaded configuration
        """
        # Search for the configuration file in the specified folder
        conf_files: List[Path] = []
        try:
            #  Get all file paths at location
            for root, _, files in os.walk(config_folder):
                conf_files.extend(Path(root).joinpath(file).resolve() for file in files)

            #  Omega load config
            loaded_conf_files: List[Union[DictConfig, ListConfig]] = [
                OmegaConf.load(file)
                for file in conf_files
                if file.suffix in [".yml", ".yaml", ".json"]
                and self._CONF_FILE_PATTERN in file.name
            ]

            if not loaded_conf_files:
                raise FileNotFoundError(f"No conf files found at {str(config_folder)}")

        except FileNotFoundError as exp:
            raise FileNotFoundError(
                f"Configuration path {str(config_folder)} provided is not correct.",
            ) from exp

        self._config = OmegaConf.merge(*loaded_conf_files)

    # TODO: do we need this?
    def find_project_root(self):
        """Returns the project's root dir"""
        # Find the root directory of the project
        current_dir = os.path.abspath(os.getcwd())
        while not os.path.exists(os.path.join(current_dir, "pyproject.toml")):
            current_dir = os.path.dirname(current_dir)
        return current_dir


_ppconfig_instance = ConfigurationParser()
load_ppconfig = _ppconfig_instance.load_ppconfig
get_ppconfig = _ppconfig_instance.get_ppconfig
