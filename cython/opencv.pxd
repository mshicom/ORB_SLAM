#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 18:04:16 2016

@author: kaihong
"""

cdef extern from "opencv2/core/core.hpp" namespace "cv":
    cdef cppclass Mat:
        Mat() except +
        void create(int, int, int)
        void* data

    cdef cppclass _InputArray:
        pass
    cdef cppclass _OutputArray:
        pass

    ctypedef const _InputArray& InputArray
    ctypedef const _OutputArray& OutputArray

    cpdef cppclass Point2f:
        float x,y

    cpdef cppclass KeyPoint:
        Point2f pt
        int octave