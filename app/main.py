from app.utils.logger import logger_system
from starlette.responses import RedirectResponse
from starlette.requests import Request
from starlette.responses import Response
from app.setup.factory import create_app
from app.config.settings import settings


app = create_app()

@app.get("/", include_in_schema=False)
def docs_redirect():
    return RedirectResponse(f"/api/{settings.general.API_V1_STR}/docs")

@app.middleware("http")
async def _add_404_middleware(request: Request, call_next):
    """Serves static assets on 404"""
    response = await call_next(request)
    path = request["path"]
    if path.startswith('/api/' + settings.general.API_V1_STR) or path.startswith("/docs"):
        return response
    if response.status_code == 404:
        return Response("You reached 404 page.")
    return response

logger_system.info("Starting uvicorn in reload mode")

if __name__ == "__main__":
    import uvicorn


    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
        port=settings.general.HOST_PORT,
    )

    logger_system.info(f"Listening at : {settings.general.HOST_PORT}")
