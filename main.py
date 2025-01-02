# main.py
from agent_manager import AgentManager
from tasks.task_scheduler import TaskScheduler
from tasks.task_executor import TaskExecutor
from agent.agent_base import AIAgent
from tasks.task_base import Task
from utils.logger import setup_logger
from utils.config_loader import load_config

def main():
    # Setup logger
    logger = setup_logger()

    # Load configuration
    config = load_config("config.json")

    # Create agent manager
    agent_manager = AgentManager()
    agent = agent_manager.create_agent("SampleAgent", config)

    # Create tasks
    task1 = Task("Sample Task")
    task1.run = lambda: logger.info("Running task...")

    # Set tasks and execute
    agent.set_tasks([task1])
    executor = TaskExecutor(agent)
    executor.execute_task(task1)

    # Schedule task
    scheduler = TaskScheduler()
    scheduler.schedule_task(task1, 5)

if __name__ == "__main__":
    main()
