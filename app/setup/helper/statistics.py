from prometheus_fastapi_instrumentator import Instrumentator
from fastapi import FastAPI


def instrument_and_expose_metrics(app: FastAPI, endpoint: str = "/manage/prometheus", tags: list = ["manage"]):
    """
    Instruments a FastAPI application for metrics monitoring and exposes the metrics via an endpoint.

    Parameters:
        app (FastAPI): The FastAPI application to be instrumented.
        endpoint (str, optional): The endpoint where metrics will be exposed. Defaults to "/manage/prometheus".
        tags (list, optional): Tags to be assigned to the exposed metrics. Defaults to ["manage"].

    Returns:
        None
    """
    Instrumentator().instrument(app).expose(app, endpoint=endpoint, tags=tags)
