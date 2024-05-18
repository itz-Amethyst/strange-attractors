import gzip
import hashlib
import pickle
import tempfile
from io import BytesIO
from typing import List , Union

from aiocache import caches
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response, StreamingResponse
from starlette.requests import Request
from app.utils.logger import logger_system as logger
from app.schemas import InitialConditionsRequest, AttractorRequestModel
from app.services.attractor import AttractorService
from app.core.attractors.functions import ATTRACTOR_FUNCTIONS
from app.services.uploader import UploadManager

router = APIRouter()
attractor_service = AttractorService()

@router.post("/initial-conditions")
async def make_initial_conditions(request: InitialConditionsRequest) -> List[float]:
    """Return a list of  initial conditions."""
    # request.percent_empty # forget for now
    if ATTRACTOR_FUNCTIONS[request.function] is None:
        raise HTTPException(
            status_code=400, detail=f"Invalid function name: {request.function}"
        )
    logger.info(f"request.function: {request.function}")
    return attractor_service.gen_random(ATTRACTOR_FUNCTIONS[request.function])


@router.post("/make-gif", response_model = None)
async def make_gif(request: Request, data: AttractorRequestModel) -> Union[Response, StreamingResponse]:
    """Make GIF."""
    if ATTRACTOR_FUNCTIONS[data.function] is None:
        raise HTTPException(
            status_code=400, detail=f"Invalid function name: {data.function}"
        )

    # Hash the initial_conditions to use as a cache key
    key = hashlib.md5(
        (str(data.initial_conditions) + data.function).encode()
    ).hexdigest()
    logger.info(f"Key: {key}")
    cache = caches.get("default")

    gif_bytes:BytesIO = None
    if cache is not None:
        gif_bytes = await cache.get(key)

    if gif_bytes is None:
        result = await cache.get(key)
        if result is not None:
            # Decompress and de-serialize the DataFrame
            with gzip.GzipFile(fileobj=BytesIO(result)) as f:
                result = pickle.load(f)

        if result is None:
            # If not in cache, perform the computation
            result = attractor_service.make_dataframe(
                initial_conditions=data.initial_conditions,
                function=ATTRACTOR_FUNCTIONS[data.function],
            )
            # Serialize and compress the DataFrame, and store it in the cache
            with BytesIO() as f:
                with gzip.GzipFile(fileobj=f, mode="w") as gz:
                    pickle.dump(result, gz)
                await cache.set(key, f.getvalue())

            logger.info(f"Set cache Key: {key}")

        gif_bytes_, filename, filesize = attractor_service.make_gif_from_df(result, cmap = data.color_map, bg_color=data.background_color )
        gif_bytes = gif_bytes_
        # Upload section
        mime , image_path , file_size = UploadManager.upload_gif(
            request = request ,
            df = result ,
            cmap = data.color_map ,
            bg_color = data.background_color ,
        )
        logger.info("gif uploaded successfully")
        await cache.set(key + "_gif", gif_bytes)  # Save the GIF content in cache

    else:
        logger.info("Retrieved GIF from cache.")

    # Check if GIF content is retrieved from cache as bytes
    if isinstance(gif_bytes , bytes):
        gif_bytes_io = BytesIO(gif_bytes)
        # Read the bytes into the BytesIO object
        gif_bytes_io.seek(0)
        gif_bytes_io.read()
        # Return the BytesIO object content in a Response
        print(gif_bytes_io.getvalue())
        return Response(content = gif_bytes_io.getvalue() , media_type = "image/gif")
    else:
        print(gif_bytes.getvalue())
        return Response(content = gif_bytes.getvalue() , media_type = "image/gif")
