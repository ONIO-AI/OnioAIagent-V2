# task_executor.py
from task_base import Task

class TaskExecutor:
    def __init__(self, agent):
        self.agent = agent

    def execute_task(self, task):
        print(f"Executing task {task.name} for agent {self.agent.name}")
        task.run()
