import os
import uuid
from fastapi import Request
from fastapi.exceptions import HTTPException
from app.config.settings import settings

from app.services.attractor import AttractorService

from app.services.backblaze import list_objects_browsable_url , upload_file , get_b2_resource

allowed_extensions = {'.gif', '.jpg', '.jpeg', '.png'}
bad_file = HTTPException(status_code=400, detail="Invalid file")
b2_rw = get_b2_resource(settings.service.ENDPOINT_URL_BUCKET, settings.service.KEY_ID_YOUR_ACCOUNT, settings.service.APPLICATION_KEY_YOUR_ACCOUNT)
attractor_service = AttractorService()

class UploadManager:

    @staticmethod
    def upload_gif(request: Request, df, cmap: str, bg_color: str):
        gif_data, original_filename, file_size_mb = attractor_service.make_gif_from_df(df, cmap, bg_color)

        if file_size_mb > 40:
            raise bad_file

        # Generate a unique filename
        unique_id = uuid.uuid4().hex[:6]
        unique_filename = f"gif_{unique_id}.gif"

        if settings.general.DEBUG:
            upload_dir = settings.service.Upload_Dir / "attractors"
            upload_dir.mkdir(parents=True, exist_ok=True)
            path = upload_dir / unique_filename

            with open(path, 'wb') as f:
                f.write(gif_data.read())

            simple_path = os.path.join(upload_dir.name, path.name)
            image_path = os.path.join(str(request.base_url), simple_path).replace('\\', '/')

        else:
            b2 = b2_rw
            path = os.path.join(settings.service.Upload_Dir_temp_for_service, unique_filename)

            with open(path, 'wb') as f:
                f.write(gif_data.read())

            upload_file(settings.service.PUBLIC_BUCKET_NAME, path, unique_filename, b2)

            image_path = f"https://{settings.service.PUBLIC_BUCKET_NAME}.{settings.service.ENDPOINT_URL_BUCKET.replace('https://','')}/{unique_filename}"

            # Remove the file in temp for better performances
            os.remove(path)

        return "image/gif", image_path, file_size_mb * 1024 * 1024

    @staticmethod
    def get_browsable_urls_in_sw3():
        return list_objects_browsable_url(bucket=settings.service.PUBLIC_BUCKET_NAME, endpoint=settings.service.ENDPOINT_URL_BUCKET, b2=b2_rw)
