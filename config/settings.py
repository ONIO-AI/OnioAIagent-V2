import os
from pathlib import Path
from typing import Dict, Any
from .config import Config
from .telegram_config import TelegramConfig
from .discord_config import DiscordConfig

class Settings:
    """Global settings for ONIO AI Agent Framework"""
    
    def __init__(self):
        self.base_config = Config()
        self.telegram_config = TelegramConfig()
        self.discord_config = DiscordConfig()
        
        # Load environment variables
        self._load_env_vars()
    
    def _load_env_vars(self):
        """Load configuration from environment variables"""
        # Override OpenAI API key if set in environment
        if os.getenv('OPENAI_API_KEY'):
            self.base_config.OPENAI_CONFIG['api_key'] = os.getenv('OPENAI_API_KEY')
            
        # Override Telegram token if set in environment
        if os.getenv('TELEGRAM_BOT_TOKEN'):
            self.telegram_config.BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
            
        # Override Discord token if set in environment
        if os.getenv('DISCORD_BOT_TOKEN'):
            self.discord_config.BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    
    def get_all_config(self) -> Dict[str, Any]:
        """Get complete configuration"""
        return {
            'base': self.base_config.get_config(),
            'telegram': self.telegram_config.get_config(),
            'discord': self.discord_config.get_config()
        }
    
    def validate_config(self) -> bool:
        """Validate all configuration settings"""
        try:
            # Check required API keys
            if not self.base_config.OPENAI_CONFIG['api_key']:
                raise ValueError("OpenAI API key is required")
                
            # Check paths
            if not self.base_config.LOGS_DIR.exists():
                self.base_config.LOGS_DIR.mkdir(parents=True)
                
            # Add more validation as needed
            return True
            
        except Exception as e:
            print(f"Configuration validation failed: {str(e)}")
            return False

# Create global settings instance
settings = Settings() 