from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.utils.logger import logger_system

router = APIRouter()


@router.get("/health")
def health_check() -> JSONResponse:
    """
    Checks the health of the project and returns a 'ping' response.
    """
    # Log the health check request
    logger_system.info("Health check endpoint was called.")

    # Return a JSON response
    return JSONResponse(content = {"message": "ping"})