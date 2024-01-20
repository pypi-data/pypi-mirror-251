from typing import Literal
import numpy as np
import cv2 as cv
import vc
import fp
from .invariant_ import hmatch, vmatch
from .. import templates as ts

_1 = int; _4 = int
def best_match(
    lines: list[np.ndarray[_1, _4]], templates: list[ts.Template1d], costs: list[float],
    axis: Literal[0, 1], verbose: bool = True, img: cv.Mat | None = None
) -> tuple[list[np.ndarray[_1, _4]], ts.Template1d, float] | None:
    """Returns `(matched_lines, template, best_cost)`
    - Displays all matches if `img is not None`
    """
    match_fn = hmatch if axis == 0 else vmatch
    best_mean_cost = float("inf")
    best_lines = None
    best_t = None
    for t, k in zip(templates, costs):
        ys = ts.coords(t.offsets)
        matched_lines, res = match_fn(lines, ys, return_all=True)
        c = res["cost"]; n = len(res["I"]); mc = k*c/n
        if verbose: print(f"Cost: {c}, Matched: {n} / {len(ys)}, Mean cost: {mc}")
        if mc < best_mean_cost and n == len(ys):
            best_mean_cost = mc
            best_lines = matched_lines
            best_t = t
    if best_lines is None:
        return None
    else:
        return best_lines, best_t, best_mean_cost