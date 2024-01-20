from typing import Callable
import numpy as np
import ramda as R
from ... import project, pq, direction
from .... import vectors as vec
from ....misc import all_pairs

_1 = int; _2 = int; _4 = int; N = int; M = int
Vec2 = np.ndarray[_2, float]


def min_proj_dist(l1: np.ndarray[_1, _4], l2: np.ndarray[_1, _4]) -> float:
    ps1 = pq(l1)
    ps2 = pq(l2)
    return min(
        *R.map(proj_dist(l1), ps2),
        *R.map(proj_dist(l2), ps1),
    )
    
def min_endpoint_dist(l1: np.ndarray[_1, _4], l2: np.ndarray[_1, _4]) -> float:
    ps1 = pq(l1)
    ps2 = pq(l2)
    return min(vec.dist(p, q) for p in ps1 for q in ps2)

def angle_diff(l1: np.ndarray[_1, _4], l2: np.ndarray[_1, _4]) -> float:
    t1 = direction(l1)
    t2 = direction(l2)
    c = np.abs(np.dot(t1, t2))
    c = np.clip(c, 0, 1) # in case of approx errors
    return np.arccos(c)

@R.curry
def proj_dist(line: np.ndarray[_1, _4], p: Vec2) -> float:
    q = project(p, line)
    return vec.dist(p, q)

def max_proj_dist(l1: np.ndarray[_1, _4], l2: np.ndarray[_1, _4]) -> float:
    p1, q1 = pq(l1)
    p2, q2 = pq(l2)
    dp2 = proj_dist(l1, p2)
    dq2 = proj_dist(l1, q2)
    dp1 = proj_dist(l2, p1)
    dq1 = proj_dist(l2, q1)
    return max(dp2, dq2, dp1, dq1)

DEFAULT_HMETRICS = [max_proj_dist]
DEFAULT_VMETRICS = [max_proj_dist]

@R.curry
def all_metrics(
    lines: np.ndarray[N, tuple[_1, _4]],
    metrics: list[Callable[np.ndarray[_1, _4], np.ndarray[_1, _4]], float]
) -> list[np.ndarray[N, N]]:
    return [all_pairs(lines, m) for m in metrics]