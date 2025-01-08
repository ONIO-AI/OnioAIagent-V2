from typing import Dict, Any
from pathlib import Path

class Config:
    """Main configuration for ONIO AI Agent Framework"""
    
    # Base paths
    BASE_DIR = Path(__file__).parent.parent
    LOGS_DIR = BASE_DIR / "logs"
    DATA_DIR = BASE_DIR / "data"
    MODELS_DIR = BASE_DIR / "models"
    
    # Application settings
    APP_NAME = "ONIO"
    VERSION = "2.0.0"
    DEBUG = True
    ENVIRONMENT = "development"
    
    # Agent settings
    AGENT_CONFIG = {
        "default_name": "ONIO_Agent",
        "max_agents": 10,
        "timeout": 3600,
        "task_interval": 30,
        "personality": {
            "tone": "friendly",
            "style": "professional",
            "language": "en"
        }
    }
    
    # OpenAI Configuration
    OPENAI_CONFIG = {
        "api_key": "your_openai_api_key",
        "model": "gpt-4",
        "temperature": 0.7,
        "max_tokens": 2000,
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0
    }
    
    # Task Configuration
    TASK_CONFIG = {
        "max_concurrent": 5,
        "timeout": 1800,
        "retry_limit": 3,
        "retry_delay": 5,
        "default_tasks": [
            "greeting",
            "help",
            "status"
        ]
    }
    
    # Logging Configuration
    LOGGING_CONFIG = {
        "level": "DEBUG",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "file": "onio.log",
        "max_size": 10485760,  # 10MB
        "backup_count": 5
    }

    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Get all configuration as dictionary"""
        return {
            key: value for key, value in cls.__dict__.items()
            if not key.startswith('_') and isinstance(value, (dict, str, int, float, bool))
        } 