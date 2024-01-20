import numpy as np
import cv2 as cv
import ramda as R
from .. import lines as ls, templates as ts, match1d, contours as cs

_1 = int; _4 = int
def acceptable(
    left: np.ndarray[_1, _4],
    right: np.ndarray[_1, _4],
    acceptable_degrees: float = 2
) -> bool:
    l_angle = np.mean(R.map(ls.angle, left))
    r_angle = np.mean(R.map(ls.angle, right))
    ldiff = abs(abs(np.rad2deg(l_angle)) - 90) # angle from vertical
    rdiff = abs(abs(np.rad2deg(r_angle)) - 90) # angle from vertical
    return ldiff < acceptable_degrees and rdiff < acceptable_degrees

def correct(
    img: cv.Mat,
    left: np.ndarray[_1, _4],
    right: np.ndarray[_1, _4],
    top: np.ndarray[_1, _4],
    bottom: np.ndarray[_1, _4],
    pad_lrtb: tuple[float, float, float, float] = (50, 50, 50, 50)
) -> cv.Mat:
    pad_left, pad_right, pad_top, pad_bot = pad_lrtb
    tl = ls.poly.mean_intersect(top, left, as_segment=False)
    tr = ls.poly.mean_intersect(top, right, as_segment=False)
    br = ls.poly.mean_intersect(bottom, right, as_segment=False)
    bl = ls.poly.mean_intersect(bottom, left, as_segment=False)
    w = int(max(abs(tl[0]-tr[0]), abs(bl[0]-br[0]))) + pad_left + pad_right
    h = int(max(abs(tl[1]-bl[1]), abs(tr[1]-br[1]))) + pad_top + pad_bot
    src = np.int32([tl, tr, br, bl])
    dst = np.int32([[pad_left, pad_top], [w-pad_right, pad_top], [w-pad_right, h-pad_bot], [pad_left, h-pad_bot]])
    M, _ = cv.findHomography(src, dst)
    return cv.warpPerspective(img, M, (w, h))

def autocorrect(
    img: cv.Mat, model: ts.SheetModel,
    min_height_p = 0.5, min_width_p = 0.5,
    filter_col_coverage = True, filter_row_coverage = True,
    return_all = False, verbose = False
) -> cv.Mat | None:
    """Autocorrect perspective via detected horizontal and vertical lines.
    - `min_{height|width}_p`: min estimated proportion of scoresheet size (w.r.t. the full image)
    - May fail (and return `None` is not enough lines are detected)"""
    height, width = img.shape[:2]
    rmin, cmin = ts.min_offsets(model)
    MIN_ROW_H = min_height_p*height*rmin
    MIN_COL_W = min_width_p*width*cmin
    cnt = cs.padded_grid(img, rmin, cmin)
    all_lines = ls.find(img)
    lines = np.int32([
        cropped for line in all_lines
            if (cropped := ls.crop(line, box=cnt)) is not None
    ])
    vlines, hlines = ls.cluster.vh(lines)
    row_lines = ls.cluster.collinear.row_cluster(hlines, height, 0.5*MIN_ROW_H)
    rows = ls.coverage.filter(row_lines, axis=0, k=2) if filter_row_coverage else row_lines
    costs = [1.2**i for i in range(len(model.rows))]
    col_lines = ls.cluster.collinear.col_cluster(vlines, width, 0.5*MIN_COL_W)
    cols = ls.coverage.filter(col_lines, axis=1)  if filter_col_coverage else col_lines
    costs = [1 for _ in model.cols]
    matched_cols, *_ = match1d.best_match(cols, model.cols, costs=costs, axis=1, verbose=verbose)
    pads = [50, 50, 50, 50]
    if len(matched_cols) < 2 or len(rows) < 2:
        return None
    corr = correct(
        img, left=cols[0], right=cols[-1],
        top=rows[0], bottom=rows[-1],
        pad_lrtb=pads
    )
    if not return_all:
        return corr
    else:
        return corr, dict(
            rows=rows, cols=matched_cols
        )
        
def autocorrect2(
    img: cv.Mat, model: ts.SheetModel,
    min_height_p = 0.5, min_width_p = 0.5,
    filter_col_coverage = True, filter_row_coverage = True,
    return_all = False, verbose = False
) -> cv.Mat | None:
    """Autocorrect perspective via detected horizontal and vertical lines.
    - Uses adaptive row clustering
    - `min_{height|width}_p`: min estimated proportion of scoresheet size (w.r.t. the full image)
    - May fail (and return `None` is not enough lines are detected)"""
    height, width = img.shape[:2]
    rmin, cmin = ts.min_offsets(model)
    MIN_ROW_H = min_height_p*height*rmin
    MIN_COL_W = min_width_p*width*cmin
    cnt = cs.padded_grid(img, rmin, cmin)
    all_lines = ls.find(img)
    lines = np.int32([
        cropped for line in all_lines
            if (cropped := ls.crop(line, box=cnt)) is not None
    ])
    vlines, hlines = ls.cluster.vh(lines)
    # row_lines = ls.cluster.collinear.row_cluster(hlines, height, 0.5*MIN_ROW_H)
    row_lines = ls.cluster.collinear2.cluster(hlines, height, MIN_ROW_H, min_clusters=model.min_rows, inclination="horizontal", n_iters=100, verbose=verbose)
    rows = ls.coverage.filter(row_lines, axis=0, k=2) if filter_row_coverage else row_lines
    costs = [1.2**i for i in range(len(model.rows))]
    col_lines = ls.cluster.collinear.col_cluster(vlines, width, 0.5*MIN_COL_W)
    cols = ls.coverage.filter(col_lines, axis=1)  if filter_col_coverage else col_lines
    costs = [1 for _ in model.cols]
    matched_cols, *_ = match1d.best_match(cols, model.cols, costs=costs, axis=1, verbose=verbose)
    pads = [50, 50, 50, 50]
    if len(matched_cols) < 2 or len(rows) < 2:
        return None
    corr = correct(
        img, left=cols[0], right=cols[-1],
        top=rows[0], bottom=rows[-1],
        pad_lrtb=pads
    )
    if not return_all:
        return corr
    else:
        return corr, dict(
            rows=rows, cols=matched_cols,
            vlines=vlines, hlines=hlines,
            matched_rows=row_lines, matched_cols=col_lines
        )