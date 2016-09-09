#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 15:42:53 2016

@author: kaihong
"""
from libcpp.vector cimport vector
from opencv cimport *

cdef extern from "../include/ORBextractor.h" namespace "ORB_SLAM":
    cdef cppclass ORBextractor:
        int HARRIS_SCORE
        int FAST_SCORE

        ORBextractor()
        ORBextractor(int)
        ORBextractor(int, float)
        ORBextractor(int, float, int)
        ORBextractor(int, float, int, int)
        ORBextractor(int, float, int, int, int)
        void extract(Mat& image,
                        Mat& mask,
                        vector[KeyPoint]& keypoints,
                        Mat& descriptors) except +


