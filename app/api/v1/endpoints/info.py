from typing import List

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.core.attractors import ATTRACTOR_FUNCTIONS
from app.schemas.request.attractor import ColorMap
from app.schemas.response.colormap import ColorMapResponse
from app.services.uploader import UploadManager

router = APIRouter()


@router.get("/list-colors", response_model = ColorMapResponse)
async def list_colors() -> ColorMapResponse:
    """Return a list of color maps."""
    return ColorMapResponse(colors=ColorMap.list_all_values())


@router.get("/list-functions")
async def list_functions() -> List[str]:
    """Return a list of functions."""
    return list(ATTRACTOR_FUNCTIONS.keys())

@router.get("/browsable-urls/")
async def get_browsable_urls():
    try:
        urls = UploadManager.get_browsable_urls_in_sw3()
        return JSONResponse(content={"success": True, "urls": urls})
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)