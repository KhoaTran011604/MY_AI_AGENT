"""
Application Settings
Centralized configuration management
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


class Settings:
    """Application settings"""

    # Application
    APP_NAME = "MY_AI_AGENT"
    APP_VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # Server
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5000))

    # MongoDB
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
    MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "chatbot_db")
    MONGODB_TIMEOUT = 5000

    # HuggingFace
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

    # Models
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    LLM_MODEL = "mistralai/Mistral-7B-Instruct-v0.3"

    # Discord (if used)
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")

    # Cache
    CACHE_ENABLED = True
    CACHE_TTL = 3600  # seconds

    @classmethod
    def get_mongodb_url(cls) -> str:
        """Get MongoDB connection URL"""
        return cls.MONGODB_URI

    @classmethod
    def get_database_name(cls) -> str:
        """Get database name"""
        return cls.MONGODB_DATABASE

    @classmethod
    def is_debug(cls) -> bool:
        """Check if debug mode is enabled"""
        return cls.DEBUG

    @classmethod
    def display_settings(cls):
        """Display current settings"""
        print(f"\n{'='*60}")
        print(f"{cls.APP_NAME} v{cls.APP_VERSION}")
        print(f"{'='*60}")
        print(f"Host: {cls.HOST}")
        print(f"Port: {cls.PORT}")
        print(f"Debug: {cls.DEBUG}")
        print(f"Database: {cls.MONGODB_DATABASE}")
        print(f"Embedding Model: {cls.EMBEDDING_MODEL}")
        print(f"LLM Model: {cls.LLM_MODEL}")
        print(f"{'='*60}\n")


# Global settings instance
settings = Settings()
