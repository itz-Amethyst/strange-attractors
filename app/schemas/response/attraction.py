from typing import List

from pydantic import BaseModel

class AttractorResponseModel(BaseModel):
    initial_conditions: List[float]