from typing import NamedTuple
import numpy as np
import cv2 as cv

_1 = int; _2 = int

class Result(NamedTuple):
    contours: list[list[np.ndarray[_1, _2]]]
    corr_img: cv.Mat
    boxes: list[cv.Mat]