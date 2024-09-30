# for updating the entity folder contents
# entity is the return type of a function
# dataclass automatically generates 
from dataclasses import dataclass
from pathlib import Path

# this annotation converts the class into a dataclass
@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir : Path
    source_URL : str
    local_data_file : Path
    unzip_dir : Path


@dataclass(frozen=True)
class DataValidationConfig:
    root_dir : Path
    STATUS_FILE : str
    ALL_REQUIRED_FILES : list