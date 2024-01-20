from typing import Callable
import numpy as np
import ramda as R

N = int; M = int; _ = int

@R.curry
def cartesian_apply(
    xs: np.ndarray[N, _], ys: np.ndarray[M, _],
    f: Callable[[np.ndarray, np.ndarray], float]
) -> np.ndarray[N, M]:
    M = np.empty((len(xs), len(ys)))
    for i, x in enumerate(xs):
        for j, y in enumerate(ys):
            M[i, j] = f(x, y)
    return M

@R.curry
def all_pairs(
    xs: np.ndarray[N, _], f: Callable[[np.ndarray, np.ndarray], float],
) -> np.ndarray[N, N]:
    n = len(xs)
    M = np.empty((n, n))
    for i in range(n):
        for j in range(i, n):
            M[i, j] = M[j, i] = f(xs[i], xs[j])
    return M