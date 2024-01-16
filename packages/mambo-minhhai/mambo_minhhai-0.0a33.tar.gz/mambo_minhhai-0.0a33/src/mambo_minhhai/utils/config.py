"""
Author: mhnguyen
"""

import yaml
from ml_collections import ConfigDict


def load_yaml(file_path: str) -> dict:
    """
    Load a yaml file and return a dictionary
    """
    with open(file_path) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config


def load_config(file_path: str) -> ConfigDict:
    """
    Load a yaml file and return a ConfigDict object, which can be accessed using dot (.)
    """
    with open(file_path) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return ConfigDict(config)
