"""
Module providing singleton class for mongodb connection.

Usage:
```
client = MongoDBConnector()
db = client.get_db()
```
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional

from settings import Settings


class MongoDBConnector:
    """Mongodb connector singleton."""
    _instance: Optional["MongoDBConnector"] = None


    def __new__(cls):
        """
        Initialize new connection or get an already existing connection.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self):
        """Initialize the database client and connector."""
        if hasattr(self, "_initialized") and self._initialized:
            return
        settings = Settings()
        self._client: AsyncIOMotorClient = AsyncIOMotorClient(settings.MONGODB_URI)
        self._db: AsyncIOMotorDatabase = self._client[settings.MONGODB_DB]


    def get_db(self) -> AsyncIOMotorDatabase:
        """Get mongo database."""
        if not hasattr(self, "_db") or self._db is None:
            raise ValueError("MongoDB client is not initialized.")
        return self._db


    def close(self):
        """Close the mongodb connection. Should be used only on shutdown event."""
        if hasattr(self, "_client") and self._client is not None:
            self._client.close()
