import cv2 as cv
from jdeskew.estimator import get_angle
from jdeskew.utility import rotate

def correct(img: cv.Mat) -> cv.Mat:
    alpha = get_angle(img)
    return rotate(img, alpha)