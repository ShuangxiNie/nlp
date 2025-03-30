import yaml
from pathlib import Path


def load_config(config_path: str) -> dict:
    """Load YAML configuration file and return as dictionary.
    
    Args:
        config_path: Path to the YAML configuration file
        
    Returns:
        dict: Parsed configuration content
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If YAML parsing fails
    """
    path = Path(config_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Config file not found at {config_path}")
        
    with open(path, 'r') as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing YAML file {config_path}") from e
