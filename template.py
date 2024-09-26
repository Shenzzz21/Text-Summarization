import os
from pathlib import Path
import logging

# logging messages with a severity level of INFO or higher (e.g., WARNING, ERROR, CRITICAL)
logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

project_name = 'textSummarizer'

list_of_files = [
    ".github/workflows/.gitkeep",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/utils/common.py",
    f"src/{project_name}/logging/__init__.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/config.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/constants/__init__.py",
    # YAML is a human-readable data serialization language that is often used for writing configuration files.
    "config/config.yaml",
    "params.yaml",
    "app.py",
    "main.py",
    "Dockerfile",
    "requirements.txt",
    "setup.py",
    "research/trials.ipynb"
]

for filepath in list_of_files:
    # convert the file path to a Path object and split it into directory and filename components
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Created directory: {filedir} for the file {filename}")

    # check if the file exists and is not empty
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        # creating empty file
        with open(filepath, 'w') as file:
            pass
            logging.info(f"Created file: {filepath}")

    else:
        logging.info(f"File {filepath} already exists and is not empty.")