#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 15:39:34 2016

@author: kaihong
"""
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

import sys
import numpy
import subprocess

proc_libs = subprocess.check_output("pkg-config --libs opencv".split())
proc_incs = subprocess.check_output("pkg-config --cflags opencv".split())

opencv_libs = [lib for lib in proc_libs.split()]
opencv_incs = [inc.partition("-I")[2]
               for inc in proc_incs.split()
               if inc.startswith("-I")]


ext_modules = [
    Extension("ORB_SLAM",
              sources = ["ORBextractor.pyx"],
              language='c++',
              include_dirs = [ "../include",
                              numpy.get_include(),]
                              + opencv_incs,
              extra_link_args = opencv_libs
)]

setup(
  name = 'orb_slam for python',
  ext_modules = cythonize(ext_modules),
)
