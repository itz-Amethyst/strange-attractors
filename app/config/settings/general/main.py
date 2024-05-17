import os
import secrets
from pathlib import Path
from typing import List , Union

from pydantic import AnyHttpUrl , field_validator
from app import __version__
from pydantic_settings import BaseSettings
from app.config.settings.helper import config

class General(BaseSettings):
    SECRET_KEY: str = secrets.token_urlsafe(32)
    DEBUG: bool = config.get("DEBUG" , True)
    VERSION: str = config.get("VERSION" , __version__)
    LOG_LEVEL: str = config.get("LOG_LEVEL" , "INFO")
    ENABLE_FILE_LOG_SYSTEM: bool = config.get("ENABLE_FILE_LOG_SYSTEM" , True)
    DOCS_FAVICON_PATH: Path = config.get("DOCS_FAVICON_PATH" , "test/fav.ico")
    HOST_PORT: int = config.get("HOST_PORT" , 8000)

    API_V1_STR: str = config.get("API_V1_STR" , "v1")

    BACKEND_CORS_ORIGINS: Union[List[AnyHttpUrl], str] = config.get("BACKEND_CORS_ORIGINS" , [])

    PROJECT_NAME: str = config.get("PROJECT_NAME" , "")

    @classmethod
    @field_validator("BACKEND_CORS_ORIGINS" , mode = "before")
    def assemble_cors_origins( cls , v: Union[str , List[str]] ) -> Union[List[str] , str]:
        if isinstance(v , str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v , (list , str)):
            return v
        raise ValueError(v)
