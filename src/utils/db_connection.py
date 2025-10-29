"""
Database Connection Utility
Manages MongoDB connections
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from src.config import settings


class MongoDBConnection:
    """MongoDB connection manager"""

    _instance = None
    _client = None

    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def connect(self):
        """
        Connect to MongoDB

        Returns:
            tuple: (client, database) or (None, None) if failed
        """
        if self._client is not None:
            return self._client, self._client[settings.get_database_name()]

        try:
            self._client = MongoClient(
                settings.get_mongodb_url(),
                serverSelectionTimeoutMS=settings.MONGODB_TIMEOUT
            )
            # Test connection
            self._client.admin.command('ping')

            database = self._client[settings.get_database_name()]
            print(f"✓ Connected to MongoDB: {settings.get_database_name()}")

            return self._client, database

        except ConnectionFailure as e:
            print(f"✗ Failed to connect to MongoDB: {e}")
            return None, None
        except Exception as e:
            print(f"✗ Error: {e}")
            return None, None

    def close(self):
        """Close MongoDB connection"""
        if self._client:
            self._client.close()
            self._client = None
            print("✓ MongoDB connection closed")

    def get_client(self):
        """Get MongoDB client"""
        if self._client is None:
            self.connect()
        return self._client

    def get_database(self):
        """Get database"""
        client = self.get_client()
        if client:
            return client[settings.get_database_name()]
        return None


# Global instance
db_connection = MongoDBConnection()
