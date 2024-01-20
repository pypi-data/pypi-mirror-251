from typing import Callable
import cv2 as cv
import numpy as np
import ramda as R
import matplotlib.pyplot as plt
import vc
import fp
import box_extraction as be
from robust_extraction import contours as cs, lines as ls, rotation as rot, vectors as vec, match1d, \
    templates as ts, perspective as pve

def pipeline5(
    img: cv.Mat, model: ts.SheetModel, min_height_p = 0.8, min_width_p = 0.8,
    filter_coverage = True, verbose = False
):
    corr_img = pve.autocorrect2(img, model)
    height, width = corr_img.shape[:2]
    rmin, cmin = ts.min_offsets(model)
    MIN_ROW_H = min_height_p*height*rmin
    MIN_COL_W = min_width_p*width*cmin
    cnt = cs.padded_grid(corr_img, rmin, cmin)
    all_lines = ls.find(corr_img)
    lines = np.int32([
        cropped for line in all_lines
            if (cropped := ls.crop(line, box=cnt)) is not None
    ])
    vlines, hlines = ls.cluster.vh(lines)
    rows = ls.cluster.collinear2.cluster(hlines, height, MIN_ROW_H, min_clusters=model.min_rows, inclination="horizontal", n_iters=100, verbose=verbose)
    cols = ls.cluster.collinear.col_cluster(vlines, width, MIN_COL_W/2)
    inlier_rows = ls.coverage.filter(rows, axis=0, k=2) if filter_coverage else rows
    inlier_cols = ls.coverage.filter(cols, axis=1)  if filter_coverage else cols
    rcosts = [1.2**i for i in range(len(model.rows))]
    matched_rows, row_t, *_ = match1d.best_match(inlier_rows, model.rows, costs=rcosts, axis=0, verbose=verbose)
    ccosts = [1 for _ in model.cols]
    matched_cols, col_t, *_ = match1d.best_match(inlier_cols, model.cols, costs=ccosts, axis=1, verbose=verbose)
    imp_rows = [matched_rows[i] for i in ts.explicit_indices(row_t.importants)]
    imp_cols = [matched_cols[i] for i in ts.explicit_indices(col_t.importants)]
    poly_rows = R.map(ls.poly.hfit(xmin=0, xmax=width), imp_rows)
    poly_cols = R.map(ls.poly.vfit(ymin=0, ymax=height), imp_cols)
    xs = ls.poly.intersect_all(poly_rows, poly_cols)
    contours = ts.contours(list(range(len(imp_rows))), model.block_cols, xs.get)
    return contours, corr_img