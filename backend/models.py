# app/models.py
from pydantic import BaseModel
from typing import List

class NumerosInput(BaseModel):
    nums: List[float]