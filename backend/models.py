# app/models.py
from pydantic import BaseModel
from typing import List, Literal

class NumerosInput(BaseModel):
    nums: List[float]

class OperacionLote(BaseModel):
    op: Literal["sum", "res", "mul", "div"]
    nums: List[float]