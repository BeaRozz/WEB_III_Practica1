from pydantic import BaseModel
from typing import List, Literal
from enum import Enum

class NumerosInput(BaseModel):
    nums: List[float]

class OperacionLote(BaseModel):
    op: Literal["sum", "res", "mul", "div"]
    nums: List[float]

class TipoOperacion(str, Enum):
    SUMA = "sum"
    RESTA = "res"
    MULTIPLICACION = "mul"
    DIVISION = "div"

class OrdenEnum(str, Enum):
    ASC = "asc"
    DESC = "desc"