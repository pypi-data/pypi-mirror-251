from typing import Callable, Iterable, NamedTuple
import numpy as np
import ramda as R
import fp
from ... import lines as ls

_1 = int; _2 = int; _4 = int; N = int; M = int

class Alignment(NamedTuple):
    i: int; j: int; k: int
    
def alignments(a: int, b: int, end: int, n: int) -> Iterable[Alignment]:
    for i in range(a+1):
        for j in range(b, end+1):
            l = j - i
            for k in range(n - l + 1):
                yield Alignment(i, j, k)

class Match(NamedTuple):
    k: int; cost: float
def matches(
    X: np.ndarray[N, float], Y: np.ndarray[M, float],
    a: int, b: int,
    metric: Callable[[np.ndarray[N, float], np.ndarray[N, float]], float]
        = lambda X, T: np.sum(np.abs(X - T)) / len(X)
) -> Iterable[Match]:
    end = min(len(X), len(Y))
    for i, j, k in alignments(a, b, end, n=len(X)):
        t = X[i]
        s = X[j] - X[i]
        T = s*Y[i:j] + t
        l = j - i
        cost = metric(X[k:k+l], T)
        yield Match(k, cost)

def contiguous(
    rows: list[np.ndarray[_1, _4]],
    template: list[float],
    importants: tuple[int, int],
    return_cost: bool = False
) -> list[np.ndarray[_1, _4]]:
    """Contiguous match. Assumptions:
    1. All true lines are detected
    2. No noisly lines are detected in-between
    """
    a, b = importants
    X = fp.vpipe(
        R.map(R.map(R.pipe(ls.midpoint, R.nth(1))), rows),
        R.map(np.mean), np.float32
    )
    k, cost = min(matches(X, template, a, b), key=R.prop("cost"))
    matched = rows[k-a:][:b]
    return (matched, cost) if return_cost else matched