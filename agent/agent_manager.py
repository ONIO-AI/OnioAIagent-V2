# agent_manager.py
from agent_base import AIAgent
from agent_config import AgentConfig
import logging

class AgentManager:
    def __init__(self):
        """
        Initialize the AgentManager with an empty agent list and a logger.
        """
        self.agents = {}  # Dictionary to hold agents by name
        self.logger = logging.getLogger("AgentManager")
        self.logger.setLevel(logging.DEBUG)

    def create_agent(self, name, config_file=None):
        """
        Create a new agent using the specified name and configuration file.
        :param name: Name of the new agent.
        :param config_file: Optional configuration file path for agent settings.
        :return: A new instance of AIAgent.
        """
        if name in self.agents:
            self.logger.warning(f"Agent with name {name} already exists. Using existing agent.")
            return self.agents[name]

        # Load agent configuration
        agent_config = AgentConfig(config_file) if config_file else AgentConfig()

        # Create a new agent
        agent = AIAgent(name, agent_config.get_config())
        self.agents[name] = agent

        self.logger.info(f"Agent '{name}' created successfully.")
        return agent

    def remove_agent(self, name):
        """
        Remove an agent by name.
        :param name: Name of the agent to remove.
        :return: True if agent is removed, False if not found.
        """
        if name in self.agents:
            del self.agents[name]
            self.logger.info(f"Agent '{name}' removed successfully.")
            return True
        else:
            self.logger.warning(f"Agent '{name}' not found. Unable to remove.")
            return False

    def list_agents(self):
        """
        List all currently active agents by name.
        :return: List of agent names.
        """
        agent_names = list(self.agents.keys())
        self.logger.info(f"Listing {len(agent_names)} agents: {agent_names}")
        return agent_names

    def get_agent(self, name):
        """
        Get an agent by name.
        :param name: Name of the agent.
        :return: AIAgent object if found, None if not.
        """
        agent = self.agents.get(name)
        if agent:
            self.logger.info(f"Agent '{name}' retrieved successfully.")
        else:
            self.logger.warning(f"Agent '{name}' not found.")
        return agent

    def update_agent(self, name, config_file):
        """
        Update an agent's configuration by name.
        :param name: Name of the agent to update.
        :param config_file: Path to the new configuration file.
        :return: True if agent updated, False if agent not found.
        """
        agent = self.get_agent(name)
        if agent:
            agent_config = AgentConfig(config_file)
            agent.config = agent_config.get_config()  # Update the agent's config
            self.logger.info(f"Agent '{name}' updated successfully.")
            return True
        else:
            self.logger.warning(f"Agent '{name}' not found. Unable to update.")
            return False

    def execute_agent_task(self, name, task_name):
        """
        Execute a specific task for a given agent by name.
        :param name: Name of the agent.
        :param task_name: Name of the task to execute.
        :return: Result of the task execution.
        """
        agent = self.get_agent(name)
        if agent:
            task = next((t for t in agent.tasks if t.name == task_name), None)
            if task:
                task.run()
                self.logger.info(f"Executed task '{task_name}' for agent '{name}'.")
            else:
                self.logger.warning(f"Task '{task_name}' not found for agent '{name}'.")
        else:
            self.logger.warning(f"Agent '{name}' not found. Task execution failed.")

    def execute_all_tasks(self):
        """
        Execute all tasks for all agents.
        :return: None
        """
        for agent in self.agents.values():
            for task in agent.tasks:
                task.run()
                self.logger.info(f"Executed task '{task.name}' for agent '{agent.name}'.")

    def get_agents_status(self):
        """
        Get the status of all agents, including tasks.
        :return: Dictionary of agent statuses.
        """
        statuses = {}
        for name, agent in self.agents.items():
            task_status = {task.name: "Completed" for task in agent.tasks}  # Simplified for example
            statuses[name] = {
                "status": "Active",
                "tasks": task_status
            }
        self.logger.info(f"Agent statuses: {statuses}")
        return statuses

