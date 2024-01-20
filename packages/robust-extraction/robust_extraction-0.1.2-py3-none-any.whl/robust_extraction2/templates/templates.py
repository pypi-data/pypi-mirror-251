from pydantic import BaseModel
from typing import Iterable, Callable
import numpy as np
import ramda as R
import fp
from .. import lines as ls

_1 = int; _2 = int; _4 = int
Vec2 = np.ndarray[_2, float]

Offsets = list[float] | tuple[int, float]
Indices = list[int] | tuple[int, int]

class Template1d(BaseModel):
    offsets: Offsets
    importants: Indices

class SheetModel(BaseModel):
    cols: list[Template1d]
    rows: list[Template1d]
    min_rows: int
    min_cols: int
    block_cols: list[int] # w.r.t. importants
    
def min_offset(offsets: Offsets) -> float:
    match offsets:
        case tuple([int(n), float(h)]):
            return h
        case _:
            return np.min(offsets)
        
def max_offset_sum(templates: list[Template1d], k: int) -> int:
    """Max sum of first/last `|k|` offsets (last if `k < 0`)"""
    if k == 0: return 0
    s = slice(0, k) if k > 0 else slice(k, None)
    return max(sum(explicit_offsets(t.offsets)[s]) for t in templates)
        
def explicit_offsets(offsets: Offsets) -> list[float]:
    match offsets:
        case tuple([int(n), float(h)]):
            return [h for _ in range(n)]
        case _:
            return offsets
        
def min_offsets(model: SheetModel) -> tuple[float, float]:
    """Returns `(row_min, col_min)`"""
    rmin = min(min_offset(t.offsets) for t in model.rows)
    cmin = min(min_offset(t.offsets) for t in model.cols)
    return rmin, cmin
    
def contiguous_boxes(
	rows: list[int],
	block_cols: list[int]
) -> Iterable[tuple[int, int]]:
	for c in block_cols:
		for r in rows:
			yield (r, c)
			yield (r, c+1)

def coords(offsets: Offsets) -> list[float]:
    match offsets:
        case tuple([int(n), float(h)]):
            return np.arange(n)*h
        case _:
            return np.cumsum([0, *offsets])
        
def length(template: Template1d) -> bool:
    return len(coords(template.offsets))
        
def explicit_indices(indices: Indices) -> list[int]:
    match indices:
        case tuple([int(start), int(end)]):
            return list(range(start, end))
        case _:
            return indices
        
@R.curry
def contour(
	row: int, col: int,
	intersect: Callable[[tuple[int, int]], Vec2]
) -> np.ndarray[_4, tuple[_1, _2]] | None:
	tl = intersect((row, col))
	tr = intersect((row, col+1))
	bl = intersect((row+1, col))
	br = intersect((row+1, col+1))
	xs = [tl, tr, br, bl]
	if any(x is None for x in xs):
		return None
	else:
		return np.int32(xs).reshape(4, 1, 2)

def contours(
    row_indices: list[int],
    block_cols: list[int],
    intersect: Callable[[tuple[int, int]], Vec2]
) -> list[np.ndarray[_4, tuple[_1, _2]] | None]:
    limits = list(contiguous_boxes(row_indices[:-1], block_cols))
    return [contour(i, j, intersect) for i, j in limits]