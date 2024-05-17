from typing import Any

from fastapi import APIRouter

from app import schemas
from app.utils.email.main import send_web_contact_email
from app.schemas import EmailContent

router = APIRouter()


@router.post("/contact", response_model=schemas.Response, status_code=201)
def send_email(*, data: EmailContent) -> Any:
    """
    Standard app contact us.
    """
    send_web_contact_email(data=data)
    return {"message": "Web contact email sent"}