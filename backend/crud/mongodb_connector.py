"""Module providing a singleton class for connecting to a MongoDB database.

This module defines a singleton class that manages a single instance of an
asynchronous MongoDB client. Using a singleton prevents the creation of multiple
client instances and provides a clean way to manage and close the connection.

Example:
    client = MongoDBConnector()
    db = client.get_db()
"""

from pymongo import AsyncMongoClient
from pymongo.database import Database
from typing import Optional

from settings import Settings


class MongoDBConnector:
    """Singleton class for managing a MongoDB connection.

    Attributes:
        _instance (Optional[MongoDBConnector]): The singleton instance.
        _client (AsyncMongoClient): Asynchronous MongoDB client.
        _db (Database): MongoDB database used by the application.
    """
    _instance: Optional["MongoDBConnector"] = None


    def __new__(cls) -> "MongoDBConnector":
        """Return the singleton instance of MongoDBConnector.

        If no instance exists, a new one is created.

        Returns:
            MongoDBConnector: The singleton instance of this class.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self) -> None:
        """Initialize the MongoDB client and database connection.

        Initialization occurs only once, even if the class is instantiated
        multiple times.
        """
        if hasattr(self, "_initialized") and self._initialized:
            return
        settings = Settings()
        self._client: AsyncMongoClient = AsyncMongoClient(settings.MONGODB_URI)
        self._db: Database = self._client[settings.MONGODB_DB]


    def get_db(self) -> Database:
        """Return the MongoDB database instance.

        Raises:
            ValueError: If the MongoDB client has not been initialized.

        Returns:
            Database: The MongoDB database instance.
        """
        if not hasattr(self, "_db") or self._db is None:
            raise ValueError("MongoDB client is not initialized.")
        return self._db


    def close(self) -> None:
        """Close the MongoDB connection.

        This method should be called once during the application's shutdown
        to properly close the connection.
        """
        if hasattr(self, "_client") and self._client is not None:
            self._client.close()
