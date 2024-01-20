from typing import Callable
from functools import partial
import numpy as np
import ramda as R
from sklearn.cluster import DBSCAN

N = int; M = int; _1 = int; _4 = int

@R.curry
def midpoint(
    hlines: np.ndarray[N, tuple[_1, _4]],
    eps: int = 25, min_samples: int = 1,
    aggregate: Callable[[list[np.ndarray[_1, _4]]], np.ndarray[_1, _4]] | None = partial(np.mean, axis=0)
) -> np.ndarray[M, tuple[_1, _4]]:
    """Cluster lines by midpoint"""
    agg = aggregate if aggregate is not None else R.identity
    ps = np.array(R.map(midpoint, hlines))
    labs = DBSCAN(eps=eps, min_samples=min_samples).fit_predict(ps)
    classes = np.unique(labs.clip(0)) # unlabeled are -1
    centers = np.int32([
        agg(hlines[np.where(labs == c)])
        for c in classes
    ])
    return centers