from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.config.settings import settings

from app.setup.helper.middleware import setup_cors_middleware
from app.setup.helper.static import serve_static_app
from app.setup.route.main import setup_routers
from app.config.logger.main import configure_logging
from app.setup.helper.statistics import instrument_and_expose_metrics
from app.setup.helper.lifespan import lifespan

tags_metadata = [
    {
        "name": "fastapi",
        "description": "fastapi project",
    },
    {
        "name": "strange-attractors",
        "description": "generate attractors based on mathematics",
    },
]

def create_app():
    configure_logging()
    description = f"{settings.general.PROJECT_NAME} API"
    app = FastAPI(
        title=settings.general.PROJECT_NAME,
        debug = settings.general.DEBUG,
        version = settings.general.VERSION,
        openapi_url=f"/api/{settings.general.API_V1_STR}/openapi.json",
        docs_url="/docs/",
        default_response_class = ORJSONResponse,
        openapi_tags = tags_metadata,
        description=description,
        redoc_url=None,
        # TOdo
        lifespan = lifespan
    )

    setup_routers(app)
    setup_cors_middleware(app)
    serve_static_app(app)
    instrument_and_expose_metrics(app)
    return app





