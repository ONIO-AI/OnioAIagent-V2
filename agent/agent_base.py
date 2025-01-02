# agent_base.py
import logging
import time
import random
from datetime import datetime
from threading import Thread
from agent_config import AgentConfig

class AgentBase:
    def __init__(self, config_file=None):
        """
        Initialize the agent base with configuration, logging, and task handling.
        :param config_file: Path to the configuration file (optional).
        """
        self.logger = logging.getLogger("AgentBase")
        self.logger.setLevel(logging.DEBUG)
        
        # Setup the configuration
        self.config = AgentConfig(config_file)
        
        # Initialize agent details
        self.agent_name = self.config.get_config().get("agent_name", "DefaultAgent")
        self.platform = self.config.get_config().get("platform", "Generic")
        self.environment = self.config.get_config().get("environment", "production")
        
        # Task execution parameters
        self.task_interval = self.config.get_config().get("task_scheduler", {}).get("interval", 30)
        self.retry_policy = self.config.get_config().get("retry_policy", {})
        
        # Task manager and state
        self.tasks = self.config.get_config().get("tasks", [])
        self.retry_count = 0
        self.running = False
        
        # Start the agent
        self.logger.info(f"Initializing {self.agent_name} on {self.platform} in {self.environment} environment.")
        
    def start(self):
        """
        Start the agent, running the tasks periodically.
        """
        self.running = True
        self.logger.info(f"{self.agent_name} is now running.")
        while self.running:
            try:
                self.run_tasks()
                time.sleep(self.task_interval)
            except Exception as e:
                self.logger.error(f"Error while running tasks: {str(e)}")
                if self.retry_count < self.retry_policy.get("max_retries", 3):
                    self.retry_count += 1
                    self.logger.info(f"Retrying... Attempt {self.retry_count}/{self.retry_policy['max_retries']}")
                    time.sleep(self.retry_policy.get("retry_interval", 5))
                else:
                    self.logger.error(f"Max retry attempts reached. Stopping agent.")
                    self.stop()
    
    def stop(self):
        """
        Stop the agent and terminate all running tasks.
        """
        self.running = False
        self.logger.info(f"{self.agent_name} has stopped.")
    
    def add_task(self, task_name, task_details):
        """
        Add a new task to the agent's task list.
        :param task_name: The name of the task.
        :param task_details: Details about the task (could be a function or a set of actions).
        """
        task = {
            "task_name": task_name,
            "task_details": task_details
        }
        self.tasks.append(task)
        self.logger.info(f"Task '{task_name}' added to the agent.")
    
    def remove_task(self, task_name):
        """
        Remove a task from the agent's task list by name.
        :param task_name: The name of the task to remove.
        """
        self.tasks = [task for task in self.tasks if task["task_name"] != task_name]
        self.logger.info(f"Task '{task_name}' removed from the agent.")
    
    def run_tasks(self):
        """
        Run all tasks in the agent's task list. This will execute tasks and handle errors.
        """
        if not self.tasks:
            self.logger.info(f"No tasks to execute for {self.agent_name}.")
            return
        
        for task in self.tasks:
            try:
                self.execute_task(task["task_name"], task["task_details"])
            except Exception as e:
                self.logger.error(f"Error executing task {task['task_name']}: {str(e)}")
    
    def execute_task(self, task_name, task_details):
        """
        Execute a specific task.
        :param task_name: Name of the task to execute.
        :param task_details: Details of the task (could be a function or other actions).
        """
        self.logger.info(f"Executing task: {task_name}")
        # Simulating task execution (could be an API call, a data fetch, etc.)
        time.sleep(random.randint(1, 5))  # Simulating variable task execution time.
        self.logger.info(f"Task '{task_name}' completed.")
    
    def get_status(self):
        """
        Get the current status of the agent.
        :return: A dictionary containing the current status of the agent (e.g., running tasks, retry count).
        """
        return {
            "agent_name": self.agent_name,
            "platform": self.platform,
            "tasks_in_progress": len(self.tasks),
            "retry_count": self.retry_count,
            "running": self.running
        }
    
    def log_status(self):
        """
        Log the current status of the agent.
        """
        status = self.get_status()
        self.logger.info(f"Agent Status - Name: {status['agent_name']}, Platform: {status['platform']}, "
                         f"Tasks in Progress: {status['tasks_in_progress']}, Retry Count: {status['retry_count']}, "
                         f"Running: {status['running']}")
    
    def periodic_log(self):
        """
        Periodically log the agent's status.
        """
        while self.running:
            self.log_status()
            time.sleep(60)  # Log status every minute.
    
    def start_periodic_logging(self):
        """
        Start periodic logging in a separate thread to avoid blocking the main thread.
        """
        log_thread = Thread(target=self.periodic_log)
        log_thread.daemon = True
        log_thread.start()
        self.logger.info("Started periodic logging thread.")
    
    def load_platform_config(self, platform_name):
        """
        Dynamically load configuration for the given platform.
        :param platform_name: Name of the platform.
        """
        self.logger.info(f"Loading platform configuration for {platform_name}...")
        # This is where you would load platform-specific configurations, 
        # like API keys, custom task logic, etc.
        # You could extend this with actual logic to load platform configurations.
    
    def update_config(self, new_config):
        """
        Update the agent's configuration.
        :param new_config: New configuration dictionary to update the agent with.
        """
        self.config.update_config(new_config)
        self.logger.info("Configuration updated.")

