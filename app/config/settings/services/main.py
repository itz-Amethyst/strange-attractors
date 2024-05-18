from pathlib import Path

from pydantic import BaseModel
from app.config.settings.helper import PROJECT_DIR as Base_Directory
from app.config.settings.helper import config


class Service(BaseModel):
    Upload_Dir: Path = Base_Directory / 'Uploads/'

    Upload_Dir_temp_for_service: Path = Base_Directory / 'temp/'

    # boto Service
    PUBLIC_BUCKET_NAME: str = config.get("PUBLIC_BUCKET_NAME", "")
    ENDPOINT_URL_BUCKET: str = config.get("ENDPOINT_URL_BUCKET", "")
    KEY_ID_YOUR_ACCOUNT: str = config.get("KEY_ID_YOUR_ACCOUNT", "")
    APPLICATION_KEY_YOUR_ACCOUNT: str = config.get("APPLICATION_KEY_YOUR_ACCOUNT", "")