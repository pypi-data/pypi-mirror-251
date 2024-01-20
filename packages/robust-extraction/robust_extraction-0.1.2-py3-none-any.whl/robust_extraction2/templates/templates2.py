from typing import NamedTuple
from pydantic import BaseModel

class Template1d(NamedTuple):
    points: list[float]
    a: int; b: int

class SheetModel2(BaseModel):
    cols: Template1d
    rows: Template1d
    block_cols: list[int]