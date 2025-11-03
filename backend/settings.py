"""
Module providing singleton class for app settings.
"""

import os
from typing import Optional


class Settings:
    """ Singleton class encapsulating all app settings. """
    _instance: Optional["Settings"] = None

    def __new__(cls):
        """ Create new class or get already existing instance. """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_settings()

        return cls._instance


    def _init_settings(self):
        """ Initialize app settings. """
        self.SECRET_KEY = os.getenv("SECRET_KEY", "SUPER_SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
        self.REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1))
        self.MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        self.MONGODB_DB: str = "brain_bridge"


    def __getattr__(self, name):
        """ Fallback method for missing attributes. """
        raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'")
