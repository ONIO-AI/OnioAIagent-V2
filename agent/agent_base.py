# agent_base.py
import logging
import time
import random
from datetime import datetime
from threading import Thread, Lock
from typing import Dict, List, Any, Optional
from agent_config import AgentConfig

class AgentBase:
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize the agent base with configuration, logging, and task handling.
        :param config_file: Path to the configuration file (optional).
        """
        # Setup logging with a better format
        self.logger = logging.getLogger("AgentBase")
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
        # Setup the configuration
        self.config = AgentConfig(config_file)
        
        # Initialize agent details with type hints
        self._load_config()
        
        # Task management
        self._task_lock = Lock()
        self.tasks: List[Dict[str, Any]] = []
        self.active_tasks: Dict[str, datetime] = {}
        self.task_history: List[Dict[str, Any]] = []
        
        # Performance metrics
        self.metrics = {
            'total_tasks_completed': 0,
            'failed_tasks': 0,
            'average_task_time': 0
        }
        
        self.logger.info(f"Initializing {self.agent_name} on {self.platform} in {self.environment} environment.")

    def _load_config(self) -> None:
        """Load configuration settings from config file"""
        config = self.config.get_config()
        self.agent_name = config.get("agent_name", "DefaultAgent")
        self.platform = config.get("platform", "Generic")
        self.environment = config.get("environment", "production")
        self.task_interval = config.get("task_scheduler", {}).get("interval", 30)
        self.retry_policy = config.get("retry_policy", {
            "max_retries": 3,
            "retry_interval": 5,
            "exponential_backoff": True
        })
        self.retry_count = 0
        self.running = False

    def start(self) -> None:
        """Start the agent with improved error handling and monitoring"""
        self.running = True
        self.start_periodic_logging()
        self.logger.info(f"{self.agent_name} is now running.")
        
        while self.running:
            try:
                self.run_tasks()
                self._cleanup_completed_tasks()
                time.sleep(self.task_interval)
            except Exception as e:
                self.logger.error(f"Error while running tasks: {str(e)}", exc_info=True)
                if not self._handle_retry():
                    break

    def _handle_retry(self) -> bool:
        """Handle retry logic with exponential backoff"""
        if self.retry_count < self.retry_policy["max_retries"]:
            self.retry_count += 1
            retry_interval = self.retry_policy["retry_interval"]
            if self.retry_policy.get("exponential_backoff"):
                retry_interval *= (2 ** (self.retry_count - 1))
            
            self.logger.info(f"Retrying in {retry_interval} seconds... "
                           f"Attempt {self.retry_count}/{self.retry_policy['max_retries']}")
            time.sleep(retry_interval)
            return True
        return False

    def execute_task(self, task_name: str, task_details: Dict[str, Any]) -> None:
        """
        Execute a specific task with improved monitoring and metrics.
        """
        start_time = time.time()
        self.active_tasks[task_name] = datetime.now()
        
        try:
            self.logger.info(f"Executing task: {task_name}")
            # Add your actual task execution logic here
            time.sleep(random.randint(1, 5))
            
            # Update metrics
            execution_time = time.time() - start_time
            with self._task_lock:
                self.metrics['total_tasks_completed'] += 1
                self.metrics['average_task_time'] = (
                    (self.metrics['average_task_time'] * (self.metrics['total_tasks_completed'] - 1) +
                     execution_time) / self.metrics['total_tasks_completed']
                )
            
            # Record task history
            self.task_history.append({
                'task_name': task_name,
                'status': 'completed',
                'execution_time': execution_time,
                'timestamp': datetime.now()
            })
            
        except Exception as e:
            self.logger.error(f"Task execution failed: {task_name}", exc_info=True)
            with self._task_lock:
                self.metrics['failed_tasks'] += 1
            self.task_history.append({
                'task_name': task_name,
                'status': 'failed',
                'error': str(e),
                'timestamp': datetime.now()
            })
            raise
        finally:
            self.active_tasks.pop(task_name, None)

    def _cleanup_completed_tasks(self) -> None:
        """Remove completed tasks that are older than the specified threshold"""
        current_time = datetime.now()
        stale_tasks = [
            task_name for task_name, start_time in self.active_tasks.items()
            if (current_time - start_time).total_seconds() > 3600  # 1 hour timeout
        ]
        
        for task_name in stale_tasks:
            self.logger.warning(f"Task {task_name} timed out and will be terminated")
            self.active_tasks.pop(task_name, None)

    def get_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        return {
            **self.metrics,
            'active_tasks': len(self.active_tasks),
            'total_tasks': len(self.tasks),
            'uptime': time.time() - self._start_time if hasattr(self, '_start_time') else 0
        }

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

