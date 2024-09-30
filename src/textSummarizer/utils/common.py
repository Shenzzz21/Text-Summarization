import os
from box.exceptions import BoxValueError
import yaml
from textSummarizer.logging import logger
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any

# ensures input data type matches arguments data type
@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    reads yaml file and returns 

    Args:
        path_to_yaml (str): path like input

    Raises:
        ValueError: if the yaml file is empty
        e: empty file

    Returns:
        ConfigBox: ConfigBox type
    """

    try:
        with open(path_to_yaml) as file:
            content = yaml.safe_load(file)
            logger.info(f"Successfully loaded yaml file: {path_to_yaml}")
            # configbox is a dict subclass that allows to access values directly using a key 
            # allows you to handle deeply nested configurations with dot notation (like accessing attributes) rather than relying on dict.get() or dict['key'] syntax
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError(f"The yaml file at {path_to_yaml} is empty.")
    except Exception as e:
        raise e
    

@ensure_annotations
def create_directories(path_to_directories: list, verbose = True):
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Created directory at: {path}")


@ensure_annotations
def get_filesize(path: Path) -> str:
    """
    returns file size in human readable format
    """
    size_in_kb = round(os.path.getsize(path) / 1024)
    return f"{size_in_kb} KB"