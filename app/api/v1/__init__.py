from fastapi import APIRouter

from app.config.settings import settings
from app.messages.api.main import JWT_ERROR_USER_REMOVED
from app.api.v1.endpoints import user, login, service

router = APIRouter(
    prefix = f'/{settings.general.API_V1_STR}',
    responses = {
        401: {
            "description": "No `Authorization` access token header, token is invalid or user removed" ,
            "content": {
                "application/json": {
                    "examples": {
                        "not authenticated": {
                            "summary": "No authorization token header" ,
                            "value": {"detail": "Not authenticated"} ,
                        } ,
                        "invalid token": {
                            "summary": "Token validation failed, decode failed, it may be expired or malformed" ,
                            "value": {"detail": "Token invalid: {detailed error msg}"} ,
                        } ,
                        "removed user": {
                            "summary": JWT_ERROR_USER_REMOVED ,
                            "value": {"detail": JWT_ERROR_USER_REMOVED} ,
                        } ,
                    }
                }
            } ,
        } ,
    }
)
router.include_router(user.router, prefix = '/users', tags = ["Users"])
router.include_router(login.router, prefix = '/login', tags = ["Login"])
router.include_router(service.router, prefix = '/service', tags = ["Service"])
