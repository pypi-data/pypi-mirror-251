from typing import Callable, Literal
from functools import partial
import numpy as np
import ramda as R
from sklearn.cluster import DBSCAN, KMeans

N = int; M = int; _1 = int; _4 = int

def axis(
    lines: np.ndarray[N, tuple[_1, _4]], axis: Literal[0, 1],
    eps: int = 10, min_samples: int = 1,
    aggregate: Callable[[list[np.ndarray[_1, _4]]], np.ndarray[_1, _4]] | None = partial(np.mean, axis=0)
) -> np.ndarray[M, tuple[_1, _4]]:
    """Cluster lines by `p[axis]`"""
    agg = aggregate if aggregate is not None else R.identity
    xs = lines[:, 0, axis] # each line = [[x0, y0, _, _]]
    labs = DBSCAN(eps=eps, min_samples=min_samples).fit_predict(xs[:, None])
    classes = np.unique(labs.clip(0)) # unlabeled are -1
    return [
        agg(lines[np.where(labs == c)])
        for c in classes
    ]