from fastapi import FastAPI

from app.setup.helper.route_name import use_route_names_as_operation_ids
from app import api
from app.api import v1


def setup_routers(app: FastAPI) -> None:
    app.include_router(api.router)
    app.include_router(v1.router)

    use_route_names_as_operation_ids(app)