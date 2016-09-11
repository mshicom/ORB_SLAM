#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 16:12:53 2016

@author: nubot
"""
import numpy as np
import matplotlib.pyplot as plt
from ORBExtractor import ORBExtractor

if __name__ == "__main__":
    e = ORBExtractor()
    im1 = np.ascontiguousarray(plt.imread("frame0000.jpg")[:,:,0])
    kp = e.extract(im1)

    plt.imshow(im1)
    [plt.plot(p.pt[0],p.pt[1],'r.') for p in kp]