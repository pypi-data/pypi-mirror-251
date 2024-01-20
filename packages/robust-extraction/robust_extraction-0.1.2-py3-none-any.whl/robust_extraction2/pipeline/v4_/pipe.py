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

_1 = int; _4 = int; N = int; _2 = int

def grid_lines(
    img: cv.Mat, model: ts.SheetModel,
    min_height_p = 0.5, min_width_p = 0.5,
    filter_coverage = True, verbose = False,
    display: Callable[[plt.Figure], None] = R.identity
) -> tuple[list[np.ndarray[_1, _4]], list[np.ndarray[_1, _4]], ts.Template1d, ts.Template1d] | None:
    """Returns `(rows, cols, row_template, col_template)`"""
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
    if verbose: display(vc.show(fp.vpipe(img, vc.draw.contours([cnt], color=(0,255,0)), vc.draw.lines(lines))))
    vlines, hlines = ls.cluster.vh(lines)
    if verbose: display(vc.show(fp.vpipe(img, vc.draw.lines(vlines), vc.draw.lines(hlines, color=(0,255,0)))))
    row_lines = ls.cluster.collinear.row_cluster(hlines, height, 0.5*MIN_ROW_H)
    col_lines = ls.cluster.collinear.col_cluster(vlines, width, 0.5*MIN_COL_W)
    inlier_rows = ls.coverage.filter(row_lines, axis=0, k=2) if filter_coverage else row_lines
    inlier_cols = ls.coverage.filter(col_lines, axis=1)  if filter_coverage else col_lines
    if verbose: display(vc.show(
        fp.vpipe(img, *[vc.draw.lines(l, color=vc.mod_color(i, 6)) for i, l in enumerate(inlier_rows)]),
        fp.vpipe(img, *[vc.draw.lines(l, color=vc.mod_color(i, 6)) for i, l in enumerate(inlier_cols)]),
    ))
    return inlier_rows, inlier_cols

def pipeline4(
    img: cv.Mat, model: ts.SheetModel, verbose = True,
    display: Callable[[plt.Figure], None] = R.identity
) -> tuple[list[np.ndarray[N, tuple[_1, _2]]], cv.Mat]:
    corr_img = pve.autocorrect(img, model)
    corr_height, corr_width = corr_img.shape[:2]
    rows, cols = grid_lines(corr_img, model, filter_coverage=False, verbose=False)
    costs = [1.2**i for i in range(len(model.rows))]
    if verbose: display(vc.show(
        ("All rows", fp.vpipe(corr_img, *[vc.draw.lines(l, color=vc.mod_color(i, 6)) for i, l in enumerate(rows)])),
        ("All cols", fp.vpipe(corr_img, *[vc.draw.lines(l, color=vc.mod_color(i, 6)) for i, l in enumerate(cols)]))
    ))
    matched_rows, row_t, *_ = match1d.best_match(rows, model.rows, costs=costs, axis=0, verbose=verbose)
    matched_cols, col_t, *_ = match1d.best_match(cols, model.cols, costs=[1], axis=1, verbose=verbose)
    if verbose: display(vc.show(
        ("Matched rows", fp.vpipe(corr_img, *[vc.draw.lines(l, color=vc.mod_color(i, 6)) for i, l in enumerate(matched_rows)])),
        ("Matched cols", fp.vpipe(corr_img, *[vc.draw.lines(l, color=vc.mod_color(i, 6)) for i, l in enumerate(matched_cols)]))
    ))
    if verbose: print(f"Matched {len(matched_rows)}, importants: {row_t.importants}")
    imp_rows = [matched_rows[i] for i in ts.explicit_indices(row_t.importants)]
    imp_cols = [matched_cols[i] for i in ts.explicit_indices(col_t.importants)]
    if verbose: display(vc.show(
        ("Important rows", fp.vpipe(corr_img, *[vc.draw.lines(l, color=vc.mod_color(i, 6)) for i, l in enumerate(imp_rows)])),
        ("Important cols", fp.vpipe(corr_img, *[vc.draw.lines(l, color=vc.mod_color(i, 6)) for i, l in enumerate(imp_cols)]))
    ))
    poly_rows = R.map(ls.poly.hfit(xmin=0, xmax=corr_width), imp_rows)
    poly_cols = R.map(ls.poly.vfit(ymin=0, ymax=corr_height), imp_cols)
    xs = ls.poly.intersect_all(poly_rows, poly_cols)
    if verbose: display(vc.show(
        # vc.draw.vertices(list(xs.values()), corr_img),
        fp.vpipe(corr_img, *[vc.draw.lines(l, color=vc.mod_color(i, 6)) for i, l in enumerate(poly_rows)]),
        fp.vpipe(corr_img, *[vc.draw.lines(l, color=vc.mod_color(i, 6)) for i, l in enumerate(poly_cols)])
    ))
    contours = ts.contours(list(range(len(imp_rows))), model.block_cols, xs.get)
    return contours, corr_img