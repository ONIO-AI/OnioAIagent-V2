# basic_agent.py
from agent_manager import AgentManager
from task_base import Task
from task_executor import TaskExecutor

class PostTask(Task):
    def __init__(self, name, message):
        super().__init__(name)
        self.message = message

    def run(self):
        print(f"Posting message: {self.message}")

# Initialize agent manager
manager = AgentManager()
config = {"task_type": "post_message", "platform": "Twitter"}

# Create an agent
agent = manager.create_agent("AI_Posting_Agent", config)

# Create and assign tasks
task1 = PostTask("Post on Twitter", "Welcome Onio World!")
agent.set_tasks([task1])

# Execute tasks
executor = TaskExecutor(agent)
executor.execute_task(task1)
