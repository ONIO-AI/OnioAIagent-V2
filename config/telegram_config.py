from typing import Dict, Any

class TelegramConfig:
    """Telegram Bot Configuration for ONIO"""
    
    # Bot Configuration
    BOT_TOKEN = "your_telegram_bot_token"
    BOT_USERNAME = "ONIO_Bot"
    
    # Chat Settings
    ALLOWED_CHATS = []  # Empty list means all chats are allowed
    GROUP_MODE = True
    PRIVATE_MODE = True
    
    # Message Configuration
    MESSAGE_CONFIG = {
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
        "disable_notification": False
    }
    
    # Command Settings
    COMMANDS = {
        "start": {
            "enabled": True,
            "description": "Start the bot",
            "response_template": "Welcome to ONIO! I'm your AI assistant."
        },
        "help": {
            "enabled": True,
            "description": "Show help message",
            "response_template": "Here are the available commands:\n{commands}"
        },
        "status": {
            "enabled": True,
            "description": "Check bot status",
            "response_template": "Bot is running. Status: {status}"
        }
    }
    
    # Rate Limiting
    RATE_LIMIT = {
        "enabled": True,
        "messages_per_minute": 60,
        "burst_limit": 5
    }
    
    # Media Settings
    MEDIA_CONFIG = {
        "allow_photos": True,
        "allow_videos": True,
        "allow_documents": True,
        "max_file_size": 20971520  # 20MB
    }

    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Get all Telegram configuration as dictionary"""
        return {
            key: value for key, value in cls.__dict__.items()
            if not key.startswith('_') and isinstance(value, (dict, str, int, float, bool, list))
        } 