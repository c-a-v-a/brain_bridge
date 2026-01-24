"""Module providing singleton class for application settings."""

import os

from typing import Optional, NoReturn


class Settings:
    """Singleton class encapsulating all application settings.

    Ensures only one instance of settings exists throughout the app.

    Attributes:
        _instance (Optional[Settings]): Holds the singleton instance of the
        class.
        SECRET_KEY (str): Secret key used for JWT encoding/decoding.
        ALGORITHM (str): Algorithm used for JWT tokens (default "HS256").
        ACCESS_TOKEN_EXPIRE_MINUTES (int): Expiration time in minutes for
        access tokens.
        REFRESH_TOKEN_EXPIRE_DAYS (int): Expiration time in days for refresh
        tokens.
        MONGODB_URI (str): MongoDB connection URI.
        MONGODB_DB (str): Name of the MongoDB database.
    """
    _instance: Optional["Settings"] = None

    def __new__(cls) -> "Settings":
        """Return the existing instance if available, otherwise create a new
        one.

        Returns:
            Settings: Singleton instance of the settings class.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_settings()

        return cls._instance


    def _init_settings(self) -> None:
        """Initialize application settings from environment variables or
        fallback to default values.
        """
        self.SECRET_KEY = os.getenv("SECRET_KEY", "SUPER_SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(
            os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
        self.REFRESH_TOKEN_EXPIRE_DAYS = int(
            os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1"))
        self.MONGODB_URI: str = os.getenv(
            "MONGODB_URI", "mongodb://localhost:27017")
        self.MONGODB_DB: str = "brain_bridge"


    def __getattr__(self, name) -> NoReturn:
        """Handle access to undefined attributes.

        Raises:
            AttributeError: Always raised for missing attributes.
        """
        raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'")
