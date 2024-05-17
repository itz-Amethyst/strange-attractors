from typing import List
from pydantic import BaseModel

from enum import Enum

class ColorMap(str, Enum):
    """Possible color map values"""

    FIRE = "fire"
    VIRIDIS = "viridis"
    CET_C1s = "CET_C1s"
    CET_C2 = "CET_C2"
    COLORWHEEL = "colorwheel"
    CET_C4s = "CET_C4s"
    BKR = "bkr"
    INFERNO = "inferno"
    BKY = "bky"
    CET_D13 = "CET_D13"
    COOLWARM = "coolwarm"
    CET_D9 = "CET_D9"
    CET_D10 = "CET_D10"
    DIVERGING_GKR_60_10_C40 = "diverging_gkr_60_10_c40"
    CET_D3 = "CET_D3"
    GWV = "gwv"
    DIVERGING_ISOLUMINANT_CJM_75_C24 = "diverging_isoluminant_cjm_75_c24"
    CET_D11 = "CET_D11"
    BJY = "bjy"
    CET_R3 = "CET_R3"
    CET_I1 = "CET_I1"
    CET_I3 = "CET_I3"
    BGY = "bgy"
    LINEAR_BGYW_15_100_C67 = "linear_bgyw_15_100_c67"
    BGYW = "bgyw"
    CET_L9 = "CET_L9"
    KBC = "kbc"
    BLUES = "blues"
    CET_L7 = "CET_L7"
    BMW = "bmw"
    BMY = "bmy"
    GRAY = "gray"
    DIMGRAY = "dimgray"
    CET_L16 = "CET_L16"
    KGY = "kgy"
    CET_L4 = "CET_L4"
    LINEAR_KRYW_5_100_C64 = "linear_kryw_5_100_c64"
    CET_CBL1 = "CET_CBL1"
    CET_CBL2 = "CET_CBL2"
    KB = "kb"
    KG = "kg"
    KR = "kr"
    CET_CBTL2 = "CET_CBTL2"
    CET_L19 = "CET_L19"
    CET_L17 = "CET_L17"
    CET_L18 = "CET_L18"
    CET_R2 = "CET_R2"
    RAINBOW = "rainbow"
    CET_R1 = "CET_R1"

class BackgroundColor(str, Enum):
    BLACK = "black"
    WHITE = "white"

class AttractorRequestModel(BaseModel):
    initial_conditions: List[float]
    color_map: ColorMap = ColorMap.BKY
    function: str = "Clifford"
    background_color: BackgroundColor = BackgroundColor.BLACK
