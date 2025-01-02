# agent_config.py
import json
import os
import logging

class AgentConfig:
    def __init__(self, config_file=None):
        """
        Initialize the AgentConfig with default values or from a configuration file.
        :param config_file: Optional path to a JSON configuration file.
        """
        self.config = {}
        self.logger = logging.getLogger("AgentConfig")
        self.logger.setLevel(logging.DEBUG)

        if config_file:
            self.load_config(config_file)
        else:
            self.set_default_config()

    def set_default_config(self):
        """
        Set the default configuration for the agent.
        """
        self.config = {
            "agent_name": "DefaultAgent",
            "platform": "Generic",
            "api_keys": {},
            "task_scheduler": {
                "interval": 30,  # Default task execution interval in seconds
                "timezone": "UTC"
            },
            "tasks": [],
            "logging": {
                "level": "DEBUG",
                "file": "agent_log.txt"
            },
            "environment": "production",  # Default environment (production or development)
            "retry_policy": {
                "max_retries": 3,
                "retry_interval": 5  # In seconds
            }
        }

    def load_config(self, config_file):
        """
        Load the configuration from a JSON file.
        :param config_file: Path to the JSON configuration file.
        """
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Configuration file {config_file} not found.")
        
        with open(config_file, 'r') as file:
            self.config = json.load(file)

        self.logger.info(f"Configuration loaded from {config_file}")

    def save_config(self, config_file):
        """
        Save the current configuration to a JSON file.
        :param config_file: Path to the file where configuration will be saved.
        """
        with open(config_file, 'w') as file:
            json.dump(self.config, file, indent=4)

        self.logger.info(f"Configuration saved to {config_file}")

    def update_config(self, new_config):
        """
        Update the configuration with new settings.
        :param new_config: Dictionary containing the new configuration settings.
        """
        self.config.update(new_config)
        self.logger.info("Configuration updated.")

    def get_config(self):
        """
        Get the current configuration as a dictionary.
        :return: Dictionary representing the current configuration.
        """
        return self.config

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

