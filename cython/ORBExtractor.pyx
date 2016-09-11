# -*- coding: utf-8 -*-
import numpy as np
cimport numpy as np # for np.ndarray
from libcpp.vector cimport vector
from cpython.ref cimport PyObject
from libcpp cimport bool
import cv2
# Function to be called at initialization
#cdef void init():
np.import_array()

cdef extern from "opencv2/core/core.hpp" namespace "cv":
    cdef cppclass Mat:
        Mat() except +
        Mat(int rows, int cols, int type, void* data) except +
        Mat(int rows, int cols, int type, void* data, size_t step=AUTO_STEP) except +
        void* data
    cdef cppclass Point2f:
        float x,y
    cdef cppclass KeyPoint:
        Point2f pt
        float size,angle,response
        int octave,class_id
    cdef int AUTO_STEP

cdef extern from "cv2.cpp":
    cdef object pyopencv_from(const Mat& m)
    cdef int pyopencv_to(object o, Mat& m) except 0



cdef extern from "../include/ORBextractor.h" namespace "ORB_SLAM":
    cdef cppclass ORBextractor:
        ORBextractor(int nfeatures, float scaleFactor, int nlevels, int scoreType, int fastTh)
        void extract(Mat& image,
                     Mat& mask,
                     vector[KeyPoint]& keypoints,
                     Mat& descriptors) except +


cdef class ORBExtractor:
    cdef ORBextractor *c_ext
    def __init__(self, nfeatures=1000, scaleFactor=1.2, nlevels=8, scoreType=0, fastTh=20):
        self.c_ext = new ORBextractor(nfeatures, scaleFactor, nlevels, scoreType, fastTh)
    def __dealloc__(self):
        del self.c_ext

    def extract(self, np.ndarray[np.uint8_t, ndim=2, mode = 'c'] image, np.ndarray[bint, ndim=2, mode = 'c'] mask=None):
        cdef vector[KeyPoint] keypoints
        cdef Mat im,msk,des

        pyopencv_to(image, im)

        if not mask is None:
            pyopencv_to(mask, msk)

        self.c_ext[0].extract(im, msk, keypoints, des)

        py_keypoints = []
        cdef KeyPoint p;
        for i in range(keypoints.size()):
            p = keypoints[i]
            py_keypoints.append(cv2.KeyPoint(p.pt.x, p.pt.y, p.size, p.angle, p.response, p.octave, p.class_id))

        return py_keypoints
