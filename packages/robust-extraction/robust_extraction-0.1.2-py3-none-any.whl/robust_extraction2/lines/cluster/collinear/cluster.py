from typing import Literal, Callable
import numpy as np
import ramda as R
import networkx as nx
import fp
from . import segment, all_metrics, DEFAULT_HMETRICS, DEFAULT_VMETRICS
from ... import midpoint

_1 = int; _4 = int; N = int

@R.curry
def hcollinear_condition(
    proj_dist: np.ndarray[tuple[N, N], float], max_d: float = 50
) -> np.ndarray[tuple[N, N], bool]:
    return proj_dist < max_d

@R.curry 
def vcollinear_condition(
    proj_dist: np.ndarray[tuple[N, N], float], max_d: float = 50
) -> np.ndarray[tuple[N, N], bool]:
    return proj_dist < max_d


Inclination = Literal["horizontal", "vertical"]
def matches(
    metrics: list[np.ndarray[N, N]],
    condition: Callable[[list[np.ndarray[N, N]]], bool]
) -> list[tuple[int, int]]:
    """Returns `[(i, j)]` s.t. `condition(metrics)[i][j]` is true"""
    return fp.vpipe(
        condition(*metrics),
        np.where, R.transpose
    )
    
def segmented_matches(
    segment_metrics: list[tuple[np.ndarray, np.ndarray, np.ndarray]],
    segments: list[list[int]],
    condition: Callable[[list[np.ndarray[N, N]]], bool] = vcollinear_condition
) -> list[tuple[int, int]]:
    """Returns `[(i, j)]` s.t. `condition(segment_metrics[s])[i'][j']` is true
    - Every `(i, j)`-pair belong to the same segment, as  `i = segments[s][i']` and `j = segments[s][j']`
    """
    res = []
    assert len(segment_metrics) == len(segments), f"len(segment_metrics) = {len(segment_metrics)} != {len(segments)} = len(segments)"
    for metrics, seg in zip(segment_metrics, segments):
        cs = matches(metrics, condition)
        reindexed_cs = [[seg[i], seg[j]] for i, j in cs]
        res += reindexed_cs
    return res
    
def row_cluster(
    lines: list[np.ndarray[_1, _4]], height: int, max_row_h: float,
    metrics: list[Callable[[np.ndarray[_1, _4], np.ndarray[_1, _4]], float]] = DEFAULT_HMETRICS,
    condition: Callable[[list[np.ndarray[tuple[N, N], float]]], np.ndarray[tuple[N, N], bool]] | None = None
) -> list[list[np.ndarray[_1, _4]]]:
    """Cluster rows based on pairwise metrics and condition
    - `metrics :: [Line]`
    """
    cond = condition or hcollinear_condition(max_d=max_row_h)
    segments = segment(lines, height, "horizontal", window_size=2.5*max_row_h)
    seg_lines = [lines[s] for s in segments]
    segment_metrics = R.map(all_metrics(metrics=metrics), seg_lines)
    E = segmented_matches(segment_metrics, segments, cond)
    G = nx.Graph(E)
    ccs = list(nx.connected_components(G))
    clusters = [
        lines[list(cc)]
        for cc in ccs
    ]
    return sorted(clusters, key=R.pipe(R.map(midpoint), R.map(R.nth(1)), np.mean))

def col_cluster(
    lines: list[np.ndarray[_1, _4]], width: int, max_col_w: float,
    metrics: list[Callable[[np.ndarray[_1, _4], np.ndarray[_1, _4]], float]] = DEFAULT_VMETRICS,
    condition: Callable[[np.ndarray[N, N], np.ndarray[N, N], np.ndarray[N, N]], bool] | None = None
) -> list[list[np.ndarray[_1, _4]]]:
    cond = condition or vcollinear_condition(max_d=max_col_w)
    segments = segment(lines, width, "vertical", window_size=width/5)
    seg_lines = [lines[s] for s in segments]
    segment_metrics = R.map(all_metrics(metrics=metrics), seg_lines)
    E = segmented_matches(segment_metrics, segments, cond)
    G = nx.Graph(E)
    ccs = list(nx.connected_components(G))
    clusters = [
        lines[list(cc)]
        for cc in ccs
    ]
    return sorted(clusters, key=lambda c: np.mean(c[:, 0, 0]))
