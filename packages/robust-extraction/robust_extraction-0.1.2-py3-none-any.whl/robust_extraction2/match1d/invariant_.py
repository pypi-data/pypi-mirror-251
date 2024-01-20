from typing import Iterable
import scipy.optimize
import numpy as np
import ramda as R
import fp
from .. import lines as ls

K = int; N = int; M = int

def alignments(k: int) -> Iterable[tuple[int, int]]:
    """Sorted 2-combinations of `[k]` (`k choose 2 = k*(k-1)/2` in total)
    - `(0, 1), (0, 2), ..., (0, k-1), (1, 2), (1, 3), ..., (1, k-1), ..., (k-2, k-1)`
    """
    for i in range(k):
        for j in range(i+1, k):
            yield i, j
      
def invariant_match(
    X: np.ndarray[K, float], Y: np.ndarray[N, float]
) -> tuple[tuple[np.ndarray[M, int], np.ndarray[M, int]], tuple[int, int]]:
    """Returns `(I, J), (s, t), (i, j), cost`
    - `X[I]` are matched with `Y[J]` (`m = min(n, k)` in total)
    - `(s, t)` are the scale and translation assigned to the match
    - The match cost (sum of absolute distances) is `sum(|X - (s*Y + t)|)`
    """
    best_I = None
    best_J = None
    best_st = None
    best_ij = None
    best_cost = float("inf")
    for i, j in alignments(len(X)):
        t = X[i]
        s = X[j] - X[i]
        Ys = s*Y + t
        C = np.abs(X[:, None] - Ys)
        I, J = scipy.optimize.linear_sum_assignment(C)
        cost = C[I, J].sum()
        if cost < best_cost:
            best_I = I; best_J = J; best_cost = cost; best_st = s, t; best_ij = i, j
            
    return (best_I, best_J), best_st, best_ij, best_cost

_1 = int; _4 = int
def hmatch(
    row_lines: list[np.ndarray[_1, _4]],
    template_rows: list[float],
    return_all: bool = False
) -> list[np.ndarray[_1, _4]]:
    """Invariant match of `row_lines` against `template_rows`, using `y` value of `row_lines` midpoints"""
    X = fp.vpipe(
        R.map(R.map(R.pipe(ls.midpoint, R.nth(1))), row_lines),
        R.map(np.mean), np.float32
    )
    (I, J), (s, t), (i, j), cost = invariant_match(X, template_rows)
    rows = [row_lines[i] for i in I]
    if return_all:
        return rows, dict(I=I, J=J, s=s, t=t, cost=cost, X=X)
    else:
        return rows

def vmatch(
    col_lines: list[np.ndarray[_1, _4]],
    template_cols: list[float],
    return_all: bool = False
) -> list[np.ndarray[_1, _4]]:
    X = fp.vpipe(
        R.map(R.map(R.pipe(ls.midpoint, R.nth(0))), col_lines),
        R.map(np.mean), np.float32
    )
    (I, J), (s, t), (i, j), cost = invariant_match(X, template_cols)
    cols = [col_lines[i] for i in I]
    if return_all:
        return cols, dict(I=I, J=J, s=s, t=t, cost=cost)
    else:
        return cols