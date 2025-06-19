import os
from dotenv import load_dotenv
from typing import Optional

class CONFIG:
    def __init__(self):
        """Initialize with None values"""
        self.bot_token: Optional[str] = None
        self.owner_id: Optional[int] = None
        self.server_url: Optional[str] = None

        self.mongodb_uri: Optional[str] = None
        self.db_name: Optional[str] = None


    def load_config(self, config_file) -> None:
        """
        Load configuration from .env file\n
        :param config_file: .env file path
        """
        load_dotenv(config_file)

        # ----- BOT CONFIGURATION -----
        self.bot_token = os.getenv("BOT_TOKEN")
        self.owner_id = int(os.getenv("OWNER_ID") or 0)
        
        # ----- DATABASE -----
        self.mongodb_uri = os.getenv("MONGODB_URI")
        self.db_name = os.getenv("DB_NAME")
    

    def validate(self) -> bool:
        """Check if required configurations are present"""
        required = [
            self.bot_token,
            self.mongodb_uri,
            self.db_name
        ]

        return all(required)
