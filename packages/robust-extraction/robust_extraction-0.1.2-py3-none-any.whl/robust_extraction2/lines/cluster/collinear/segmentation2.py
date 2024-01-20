from typing import Literal
import numpy as np
import fp

N = int; _1 = int; _4 = int

def window(sorted_xs: list[float], win_size: float, width: float) -> list[list[int]]:
    """Classify `sorted_xs` into equal sized interval windows. Returns `W = [W1, ..., Wk]` s.t:
    - For each window `Wj`, `i in Wj` iff `xs[i]` belongs to window `j`
    """
    n_windows = int(np.ceil(width/win_size))
    i = 0 # xs
    j = 0 # windows
    windows = [[] for _ in range(n_windows)]
    while i < len(sorted_xs) and j < n_windows:
        if sorted_xs[i] < (j+1)*win_size:
            windows[j] += [i]
            i += 1
        else:
            j += 1
    return windows

def overlapped_window(sorted_xs: np.ndarray[N, float], win_size: float, width: float) -> list[list[int]]:
    """Classify `sorted_xs` into equal sized overlapping intervals. Each `x` is classified into 1 or 2 windows
    - Returns `W = [W1, ..., Wk]` s.t: for each window `Wj`, `i in Wj` iff `xs[i]` belongs to window `j`
    """
    indices = np.argsort(sorted_xs)
    half_windows = window(sorted_xs[indices], win_size=win_size/2, width=width)
    windows = [[] for _ in range(len(half_windows)-1)]
    windows[0] = half_windows[0]
    for i, hw in fp.skip(1, enumerate(half_windows[:-1])):
        reindexed = [indices[j] for j in hw]
        windows[i-1] += reindexed
        windows[i] += reindexed
    windows[-1] += half_windows[-1]
    return windows

# def segment(lines: list[np.ndarray[_1, _4]], size: float, inclination: Literal["vertical", "horizontal"], window_size: int) -> list[list[int]]:
#     """Segment lines by windows of `window_size` height/width. Each segment is a set of line indices"""
#     axis = 0 if inclination == "vertical" else 1 # vertical lines are clustered by x; horizontal by y
#     n_windows = int(np.ceil(size/window_size))
#     xs = np.int32(R.map(R.pipe(midpoint, R.nth(axis)), lines))
#     windows = overlapping_windows(window_size, n_windows)
#     return classify(xs, windows)
