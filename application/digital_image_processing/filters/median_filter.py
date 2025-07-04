#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Implementation of median filter algorithm
"""

from cv2 import COLOR_BGR2GRAY
from cv2 import cvtColor
from cv2 import imread
from cv2 import imshow
from cv2 import waitKey
from numpy import divide
from numpy import int8
from numpy import multiply
from numpy import ravel
from numpy import sort
from numpy import zeros_like

def median_filter(gray_img, mask=3):
    """
    :param gray_img: gray image
    :param mask: mask size
    :return: image with median filter
    """
    # set image borders
    bd = int(mask / 2)
    # copy image size
    median_img = zeros_like(gray)
    for i in range(bd, gray_img.shape[0] - bd):
        for j in range(bd, gray_img.shape[1] - bd):
            # get mask according with mask
            kernel = ravel(gray_img[i - bd:i + bd + 1, j - bd:j + bd + 1])
            # calculate mask median
            median = sort(kernel)[int8(divide((multiply(mask, mask)), 2) + 1)]
            median_img[i, j] = median
    return median_img

if __name__ == '__main__':
    # read original image
    img = imread('lena.jpg')
    # turn image in gray scale value
    gray = cvtColor(img, COLOR_BGR2GRAY)

    # get values with two different mask size
    median3x3 = median_filter(gray, 3)
    median5x5 = median_filter(gray, 5)

    # show result images
    imshow('median filter with 3x3 mask', median3x3)
    imshow('median filter with 5x5 mask', median5x5)
    waitKey(0)