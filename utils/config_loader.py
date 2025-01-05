# config_loader.py
import json
import yaml
import toml
import logging
from typing import Dict, Any, Optional, Union
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

class ConfigLoader:
    """Configuration loader supporting multiple file formats (JSON, YAML, TOML)"""
    
    SUPPORTED_FORMATS = {
        '.json': 'json',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.toml': 'toml'
    }

    def __init__(self, default_config: Optional[Dict[str, Any]] = None):
        """
        Initialize the config loader.
        :param default_config: Optional default configuration
        """
        self.default_config = default_config or {}
        self._setup_logging()
        self._last_loaded: Optional[datetime] = None
        self._current_config: Dict[str, Any] = {}

    def _setup_logging(self) -> None:
        """Setup logging configuration"""
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    def load_config(self, file_path: Union[str, Path], validate: bool = True) -> Dict[str, Any]:
        """
        Load configuration from file with format auto-detection.
        
        :param file_path: Path to configuration file
        :param validate: Whether to validate the configuration
        :return: Loaded configuration dictionary
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")

        format_type = self.SUPPORTED_FORMATS.get(file_path.suffix.lower())
        if not format_type:
            raise ValueError(
                f"Unsupported file format: {file_path.suffix}. "
                f"Supported formats: {', '.join(self.SUPPORTED_FORMATS.keys())}"
            )

        try:
            config = self._load_by_format(file_path, format_type)
            
            if validate:
                self._validate_config(config)
            
            # Merge with default config
            merged_config = self._deep_merge(self.default_config.copy(), config)
            
            self._current_config = merged_config
            self._last_loaded = datetime.fromtimestamp(file_path.stat().st_mtime)
            
            logger.info(f"Successfully loaded configuration from {file_path}")
            return merged_config

        except Exception as e:
            logger.error(f"Error loading configuration from {file_path}: {str(e)}")
            raise

    def _load_by_format(self, file_path: Path, format_type: str) -> Dict[str, Any]:
        """Load configuration based on file format"""
        with file_path.open('r', encoding='utf-8') as f:
            if format_type == 'json':
                return json.load(f)
            elif format_type == 'yaml':
                return yaml.safe_load(f)
            elif format_type == 'toml':
                return toml.load(f)
            
        raise ValueError(f"Unsupported format type: {format_type}")

    def save_config(self, config: Dict[str, Any], file_path: Union[str, Path], 
                   format_type: Optional[str] = None) -> None:
        """
        Save configuration to file with backup creation.
        
        :param config: Configuration to save
        :param file_path: Path to save the configuration
        :param format_type: Optional format override
        """
        file_path = Path(file_path)
        
        # Determine format type
        format_type = format_type or self.SUPPORTED_FORMATS.get(file_path.suffix.lower())
        if not format_type:
            raise ValueError(f"Cannot determine format for file: {file_path}")

        # Create backup if file exists
        if file_path.exists():
            backup_path = file_path.with_suffix(f'.backup_{datetime.now():%Y%m%d_%H%M%S}')
            file_path.rename(backup_path)
            logger.info(f"Created backup at {backup_path}")

        try:
            with file_path.open('w', encoding='utf-8') as f:
                if format_type == 'json':
                    json.dump(config, f, indent=4)
                elif format_type == 'yaml':
                    yaml.safe_dump(config, f)
                elif format_type == 'toml':
                    toml.dump(config, f)
                    
            logger.info(f"Configuration saved to {file_path}")

        except Exception as e:
            logger.error(f"Error saving configuration: {str(e)}")
            # Restore from backup if available
            if 'backup_path' in locals() and backup_path.exists():
                backup_path.rename(file_path)
                logger.info("Restored from backup after save failure")
            raise

    def _deep_merge(self, dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively merge two dictionaries.
        :return: Merged dictionary
        """
        for key, value in dict2.items():
            if (
                key in dict1 
                and isinstance(dict1[key], dict) 
                and isinstance(value, dict)
            ):
                dict1[key] = self._deep_merge(dict1[key], value)
            else:
                dict1[key] = value
        return dict1

    def _validate_config(self, config: Dict[str, Any]) -> None:
        """
        Validate configuration structure and required fields.
        Raise ValueError if validation fails.
        """
        required_fields = {
            'agent_name': str,
            'environment': str,
            'logging': dict
        }

        for field, expected_type in required_fields.items():
            if field not in config:
                raise ValueError(f"Missing required field: {field}")
            if not isinstance(config[field], expected_type):
                raise ValueError(
                    f"Invalid type for {field}. Expected {expected_type.__name__}, "
                    f"got {type(config[field]).__name__}"
                )

    def reload_if_modified(self, file_path: Union[str, Path]) -> bool:
        """
        Check if config file has been modified and reload if necessary.
        :return: True if config was reloaded, False otherwise
        """
        file_path = Path(file_path)
        if not file_path.exists():
            return False

        last_modified = datetime.fromtimestamp(file_path.stat().st_mtime)
        if self._last_loaded and last_modified > self._last_loaded:
            self.load_config(file_path)
            return True
        return False

    @property
    def current_config(self) -> Dict[str, Any]:
        """Get current configuration"""
        return self._current_config.copy()
