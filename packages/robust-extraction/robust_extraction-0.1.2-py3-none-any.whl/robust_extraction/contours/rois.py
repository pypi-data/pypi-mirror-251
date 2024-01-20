import numpy as np
import cv2 as cv
import ramda as R

_1 = int; _2 = int
@R.curry
def roi(
    contour: list[np.ndarray[_1, _2]], img: cv.Mat,
    pad_lrtb: tuple[float, float, float, float] = (0, 0, .15, .25)
) -> cv.Mat:
    """- `pad_lrtb`: proportions of height/width to add as padding"""
    l, r, t, b = pad_lrtb
    x, y, w, h = cv.boundingRect(contour)
    top = int(y - t*h)
    bot = int(y + (1+b)*h)
    left = int(x - l*w)
    right = int(x + (1+r)*w)
    return img[top:bot, left:right]