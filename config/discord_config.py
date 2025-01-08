from typing import Dict, Any

class DiscordConfig:
    """Discord Bot Configuration for ONIO"""
    
    # Bot Configuration
    BOT_TOKEN = "your_discord_bot_token"
    APPLICATION_ID = "your_application_id"
    PUBLIC_KEY = "your_public_key"
    
    # Server Settings
    ALLOWED_SERVERS = []  # Empty list means all servers are allowed
    DEFAULT_PREFIX = "!"
    
    # Permission Configuration
    PERMISSIONS = {
        "send_messages": True,
        "read_messages": True,
        "embed_links": True,
        "attach_files": True,
        "read_message_history": True,
        "mention_everyone": False,
        "use_external_emojis": True,
        "add_reactions": True
    }
    
    # Command Settings
    COMMANDS = {
        "help": {
            "enabled": True,
            "description": "Show help message",
            "category": "General"
        },
        "status": {
            "enabled": True,
            "description": "Check bot status",
            "category": "System"
        },
        "chat": {
            "enabled": True,
            "description": "Chat with the AI",
            "category": "AI"
        }
    }
    
    # Channel Configuration
    CHANNEL_CONFIG = {
        "allowed_types": ["text", "news", "forum"],
        "log_channel": None,
        "welcome_channel": None,
        "admin_channel": None
    }
    
    # Message Settings
    MESSAGE_CONFIG = {
        "max_length": 2000,
        "delete_command_after": False,
        "use_embeds": True,
        "default_color": 0x3498db
    }

    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Get all Discord configuration as dictionary"""
        return {
            key: value for key, value in cls.__dict__.items()
            if not key.startswith('_') and isinstance(value, (dict, str, int, float, bool, list))
        } 