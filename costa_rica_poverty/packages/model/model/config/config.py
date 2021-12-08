from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel
from strictyaml import YAML, load
import datetime as dt

import model

# DIRECTORY PATHS
"""
This section defines the directory structure for consistent 
use in modules across the package.
"""

TODAY = dt.datetime.today().strftime("%Y-%m-%d")

#PACKAGE_ROOT = pathlib.Path().resolve()
PACKAGE_ROOT = Path(model.__file__).resolve().parent
ROOT = PACKAGE_ROOT.parent
INPUT_DIR = f"{PACKAGE_ROOT}/input"
ASSET_DIR = f"{PACKAGE_ROOT}/assets"
OUTPUT_DIR = f"{PACKAGE_ROOT}/output"
CONFIG_FILE_PATH = ROOT/"config.yml"


class PackageConfig(BaseModel):
    """
    Package information config.
    """

    package_name: str
    raw_data: str
    processed_data: str
    train_data_file: Optional[str]
    test_data_file: Optional[str]
    preprocess_pipeline_name: Optional[str]
    analysis_pipeline_name: Optional[str]
    process_log_file: str


class ModelConfig(BaseModel):
    """
    All configurations pertaining to
    data processing and model fitting.
    """

    primary_dependent_variables: List[str]
    variables_to_include: List[str]
    variance_threshold: Optional[float]
    alpha: Optional[float]
    random_state: int
    test_size: Optional[float]

class Config(BaseModel):
    ''' 
    Core config object.
    Collects config.yml, PackageConfig, ModelConfig.
    '''

    package_config: PackageConfig
    model_config: ModelConfig

def detect_config_file() -> Path:
    '''
    Identify configuration.yml.
    '''
    if CONFIG_FILE_PATH.is_file():
        return CONFIG_FILE_PATH
    else:
        raise Exception(f"Config.yml not found in {CONFIG_FILE_PATH}")

def extract_configurations_from_yml(config_path: Path = None) -> YAML:
    '''
    Parse YAML for package and model configurations.
    '''

    if not config_path:
        config_path = detect_config_file()
    if config_path:
        with open(config_path, 'r') as config_file:
            parsed_config_file = load(config_file.read())
            return parsed_config_file
    else:
        raise OSError(f"No configuration fle found in {config_path}")

def create_and_validate_configurations(parsed_config_file: YAML = None) -> Config:
    '''
    Run valdidation procedure for configuration information.
    '''
    if parsed_config_file is None:
        parsed_config_file = extract_configurations_from_yml()
    
    _config = Config(
        package_config=PackageConfig(**parsed_config_file.data),
        model_config=ModelConfig(**parsed_config_file.data)
    )

    return _config

config = create_and_validate_configurations()