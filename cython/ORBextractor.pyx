# -*- coding: utf-8 -*-
import numpy as np
cimport numpy as np # for np.ndarray
from libcpp.vector cimport vector
cimport ORBextractor as orb
from cpython.ref cimport PyObject


# Declares the official wrapper conversion functions + NumPy's import_array() function
cdef extern from "cv2.cpp":
    void import_array()
    PyObject* pyopencv_from(const Mat&)
    int pyopencv_to(PyObject*, Mat&)

# Function to be called at initialization
cdef void init():
    np.import_array()

# Python to C++ conversion
cdef Mat nparrayToMat(object array):
    cdef Mat mat
    cdef PyObject* pyobject = <PyObject*> array
    pyopencv_to(pyobject, mat)
    return <Mat> mat

# C++ to Python conversion
cdef object matToNparray(Mat mat):
    return <object> pyopencv_from(mat)



cdef class ORBExtractor:
    cdef orb.ORBextractor *c_ext
    def __cinit__(self, nfeatures, scaleFactor, nlevels, scoreType, fastTh):
        self.c_ext = new orb.ORBextractor(nfeatures, scaleFactor, nlevels, scoreType, fastTh)
    def __dealloc__(self):
        del self.c_ext

    def extract(self, np.ndarray image, np.ndarray mask=None):
        cdef vector[KeyPoint] keypoints
        cdef Mat des,msk
        if mask is None:
            self.c_ext[0].extract(nparrayToMat(image), msk, keypoints, des)
        else:
            self.c_ext[0].extract(nparrayToMat(image), nparrayToMat(image), keypoints, des)
        return <object> keypoints
