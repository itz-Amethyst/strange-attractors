from typing import List
from pydantic import BaseModel
class ColorMapResponse(BaseModel):
    colors: List[str]