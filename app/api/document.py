from app.config.settings import settings
from fastapi import APIRouter
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.responses import HTMLResponse

router = APIRouter()

# Override the documentation endpoint to serve a customized version
@router.get(f"/{settings.general.API_V1_STR}/docs", include_in_schema=False)
async def get_docs_v1() -> HTMLResponse:
    """A custom route to override the default swagger UI for the v1 API."""
    return get_swagger_ui_html(
        openapi_url=f"/api/{settings.general.API_V1_STR}/openapi.json",
        title=f"{settings.general.PROJECT_NAME} | Documentation",
        swagger_favicon_url=settings.general.DOCS_FAVICON_PATH,
    )