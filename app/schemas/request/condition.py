from pydantic import BaseModel
class InitialConditionsRequest(BaseModel):
    function: str = "Clifford"  # default value
    percent_empty: float = 0.0