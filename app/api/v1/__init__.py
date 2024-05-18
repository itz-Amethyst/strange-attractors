from fastapi import APIRouter

from app.config.settings import settings
from app.api.v1.endpoints import info, main

router = APIRouter(
    prefix = f'/{settings.general.API_V1_STR}/attractors',
)
router.include_router(info.router, tags = ["Info"])
router.include_router(main.router, tags = ["attractors"])
