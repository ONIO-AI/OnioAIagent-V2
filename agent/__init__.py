# __init__.py
"""
This package contains all the core components needed to create and manage AI agents.
The core classes for agent creation and management are found in agent_base.py and agent_manager.py.
"""

# Import necessary modules and classes for easy access when importing the package
from .agent_base import AIAgent
from .agent_manager import AgentManager
from .agent_config import AgentConfig
