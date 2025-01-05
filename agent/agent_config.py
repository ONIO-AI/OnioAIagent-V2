# agent_config.py
import json
import os
import logging
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime

class AgentConfig:
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize the AgentConfig with default values or from a configuration file.
        :param config_file: Optional path to a JSON configuration file.
        """
        self.config: Dict[str, Any] = {}
        self._setup_logging()
        self._config_file = config_file
        self._last_modified: Optional[datetime] = None
        
        if config_file:
            self.load_config(config_file)
        else:
            self.set_default_config()

    def _setup_logging(self) -> None:
        """Setup logging with proper formatting"""
        self.logger = logging.getLogger("AgentConfig")
        self.logger.setLevel(logging.DEBUG)
        
        if not self.logger.handlers:
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def set_default_config(self) -> None:
        """Set the default configuration for the agent."""
        self.config = {
            "agent_name": "DefaultAgent",
            "platform": "Generic",
            "api_keys": {},
            "task_scheduler": {
                "interval": 30,
                "timezone": "UTC",
                "max_concurrent_tasks": 5,
                "task_timeout": 3600  # 1 hour
            },
            "tasks": [],
            "logging": {
                "level": "DEBUG",
                "file": "agent_log.txt",
                "max_size": 10485760,  # 10MB
                "backup_count": 5
            },
            "environment": "production",
            "retry_policy": {
                "max_retries": 3,
                "retry_interval": 5,
                "exponential_backoff": True,
                "max_retry_interval": 300  # 5 minutes
            },
            "monitoring": {
                "enabled": True,
                "metrics_interval": 60,
                "alert_threshold": 0.8  # 80% resource usage
            },
            "security": {
                "enable_encryption": True,
                "key_rotation_interval": 86400,  # 24 hours
                "allowed_ips": []
            }
        }

    def load_config(self, config_file: str) -> None:
        """
        Load the configuration from a JSON file with validation.
        :param config_file: Path to the JSON configuration file.
        """
        config_path = Path(config_file)
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file {config_file} not found.")
        
        try:
            with config_path.open('r') as file:
                new_config = json.load(file)
            
            # Validate and merge with defaults
            self.set_default_config()
            self._merge_configs(new_config)
            
            self._last_modified = datetime.fromtimestamp(config_path.stat().st_mtime)
            self.logger.info(f"Configuration loaded from {config_file}")
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in config file: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            raise

    def _merge_configs(self, new_config: Dict[str, Any]) -> None:
        """
        Recursively merge new configuration with existing config.
        :param new_config: New configuration to merge.
        """
        for key, value in new_config.items():
            if (
                key in self.config 
                and isinstance(self.config[key], dict) 
                and isinstance(value, dict)
            ):
                self._merge_configs(value)
            else:
                self.config[key] = value

    def save_config(self, config_file: Optional[str] = None) -> None:
        """
        Save the current configuration to a JSON file with backup.
        :param config_file: Path to the file where configuration will be saved.
        """
        save_path = Path(config_file or self._config_file)
        
        # Create backup of existing config
        if save_path.exists():
            backup_path = save_path.with_suffix(f'.backup_{datetime.now():%Y%m%d_%H%M%S}')
            save_path.rename(backup_path)
            self.logger.info(f"Created backup at {backup_path}")
        
        try:
            with save_path.open('w') as file:
                json.dump(self.config, file, indent=4)
            self.logger.info(f"Configuration saved to {save_path}")
            
        except Exception as e:
            self.logger.error(f"Error saving config: {e}")
            if backup_path.exists():
                backup_path.rename(save_path)
                self.logger.info("Restored from backup after save failure")
            raise

    def update_config(self, new_config: Dict[str, Any], save: bool = True) -> None:
        """
        Update the configuration with new settings and optionally save.
        :param new_config: Dictionary containing the new configuration settings.
        :param save: Whether to save the updated config to file.
        """
        self._merge_configs(new_config)
        self.logger.info("Configuration updated.")
        
        if save and self._config_file:
            self.save_config()

    def get_config(self) -> Dict[str, Any]:
        """
        Get the current configuration as a dictionary.
        :return: Dictionary representing the current configuration.
        """
        return self.config.copy()  # Return a copy to prevent direct modification

    def reload_if_modified(self) -> bool:
        """
        Reload config if the file has been modified.
        :return: True if config was reloaded, False otherwise.
        """
        if not self._config_file:
            return False
            
        config_path = Path(self._config_file)
        if not config_path.exists():
            return False
            
        last_modified = datetime.fromtimestamp(config_path.stat().st_mtime)
        if self._last_modified and last_modified > self._last_modified:
            self.load_config(self._config_file)
            return True
        return False

    def get_api_key(self, platform_name):
        """
        Get the API key for a specific platform (e.g., Twitter, Google, etc.)
        :param platform_name: Name of the platform for which to get the API key.
        :return: The API key associated with the platform.
        """
        return self.config.get("api_keys", {}).get(platform_name, None)

    def set_api_key(self, platform_name, api_key):
        """
        Set the API key for a specific platform.
        :param platform_name: Name of the platform.
        :param api_key: The API key to set.
        """
        if "api_keys" not in self.config:
            self.config["api_keys"] = {}
        self.config["api_keys"][platform_name] = api_key
        self.logger.info(f"API key for {platform_name} set.")

    def set_task_scheduler(self, interval, timezone="UTC"):
        """
        Set or update the task scheduler configuration.
        :param interval: Interval (in seconds) for task execution.
        :param timezone: Timezone for scheduling (default is UTC).
        """
        self.config["task_scheduler"] = {
            "interval": interval,
            "timezone": timezone
        }
        self.logger.info(f"Task scheduler set to {interval} seconds, timezone {timezone}.")

    def add_task(self, task_name, task_details):
        """
        Add a new task to the agent configuration.
        :param task_name: Name of the task.
        :param task_details: Details of the task (a dictionary).
        """
        task = {
            "task_name": task_name,
            "task_details": task_details
        }
        self.config["tasks"].append(task)
        self.logger.info(f"Task '{task_name}' added.")

    def remove_task(self, task_name):
        """
        Remove a task by its name from the agent configuration.
        :param task_name: Name of the task to remove.
        """
        self.config["tasks"] = [task for task in self.config["tasks"] if task["task_name"] != task_name]
        self.logger.info(f"Task '{task_name}' removed.")

    def set_environment(self, environment):
        """
        Set the environment for the agent (e.g., production or development).
        :param environment: The environment to set.
        """
        self.config["environment"] = environment
        self.logger.info(f"Environment set to {environment}.")

    def set_retry_policy(self, max_retries, retry_interval):
        """
        Set the retry policy for tasks that fail.
        :param max_retries: Maximum number of retries.
        :param retry_interval: Interval between retries in seconds.
        """
        self.config["retry_policy"] = {
            "max_retries": max_retries,
            "retry_interval": retry_interval
        }
        self.logger.info(f"Retry policy set: Max retries = {max_retries}, Retry interval = {retry_interval} seconds.")

    def get_logging_config(self):
        """
        Get the logging configuration (level and file).
        :return: Dictionary representing the logging configuration.
        """
        return self.config.get("logging", {})

    def update_logging_config(self, level=None, log_file=None):
        """
        Update logging configuration.
        :param level: Log level (e.g., DEBUG, INFO, ERROR).
        :param log_file: Log file path.
        """
        if level:
            self.config["logging"]["level"] = level
        if log_file:
            self.config["logging"]["file"] = log_file
        self.logger.info("Logging configuration updated.")

    def load_platform_config(self, platform_name):
        """
        Load platform-specific configuration, if available.
        :param platform_name: The platform for which to load configuration.
        """
        platform_config_path = f"platform_configs/{platform_name}_config.json"
        if os.path.exists(platform_config_path):
            with open(platform_config_path, 'r') as file:
                platform_config = json.load(file)
            self.update_config(platform_config)
            self.logger.info(f"Loaded platform-specific configuration for {platform_name}.")
        else:
            self.logger.warning(f"No platform-specific configuration found for {platform_name}. Using default.")

