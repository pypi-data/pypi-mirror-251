from typing import Literal
import numpy as np
import ramda as R
import fp
from . import pq, xintersect, yintersect, intersect, project

_1 = int; _4 = int

@R.curry
def contained(l1: np.ndarray[_1, _4], l2: np.ndarray[_1, _4], axis: Literal[0, 1]) -> bool:
    """Is the `axis` projection of `l1` contained in the projection of `l2`?"""
    p1, q1 = pq(l1)
    p2, q2 = pq(l2)
    return p2[axis] <= p1[axis] and q1[axis] <= q2[axis]

@R.curry
def remove_contained(lines: list[np.ndarray[_1, _4]], axis: Literal[0, 1]) -> list[np.ndarray[_1, _4]]:
    [l1, *lns] = lines
    result = [l1]
    for l2 in lns:
        if not contained(l2, l1, axis=axis):
            result += [l2]
            l1 = l2
    return np.int32(result)

@R.curry
def join(lines: list[np.ndarray[_1, _4]], Vmin: float, Vmax: float, axis: Literal[0, 1]) -> list[np.ndarray[_1, _4]]:
    """Extend `lines` to form a continuous polyline in `[Vmin, Vmax]`"""
    ax_intersect = xintersect if axis == 0 else yintersect
    slines = sorted(lines, key=lambda l: l[0][axis])
    [l1, *_] = slines
    p1 = [Vmin, ax_intersect(l1, Vmin)]
    points = [p1 if axis == 0 else np.flip(p1)]
    for l1, l2 in fp.pairwise(slines):
        _, q1 = pq(l1)
        p2, _ = pq(l2)
        if q1[axis] < p2[axis]: # a) non-overlapping
            points += [q1, p2]
        elif (x := intersect(l1, l2)) is not None:
            points += [x]
        else:
            x1 = project(p2, l1)
            x2 = project(q1, l2)
            points += [x1, x2]
    
    l = slines[-1]
    p = [Vmax, ax_intersect(l, Vmax)]
    points += [p if axis == 0 else np.flip(p)]
    lines = [
        [[*p, *q]]
        for p, q in fp.pairwise(points)
    ]
    return np.int32(lines)
