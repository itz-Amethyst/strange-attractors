from functools import lru_cache
from pydantic_settings import BaseSettings

from app.config.settings.general.main import General
from app.config.settings.services.main import Service



class Settings(BaseSettings):

    general: General = General()
    service: Service = Service()

@lru_cache(maxsize = 1)
def get_settings() -> Settings:
    return Settings()

