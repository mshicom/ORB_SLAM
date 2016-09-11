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

    px,py = zip(*[p.pt for p in kp])
    plt.imshow(im1)
    plt.plot(px,py,'r.')


#%%
    import os
    os.chdir('/home/nubot/data/workspace/gltes')
    from tools import *
    from  scipy.ndimage import distance_transform_edt

    class Frame:
        def __init__(self, im):
            self.im = np.ascontiguousarray(im)
            self.extractKP()

        def extractKP(self):
            kp = e.extract(self.im)
            self.px,self.py = np.atleast_1d(zip(*[p.pt for p in kp]))

        def calcDT(self):
            x,y = np.asarray(self.px,'i'), np.asarray(self.py,'i')
            f_ = np.full_like(self.im, 1e10, 'f')
            f_[y,x] = 0

            self.d0 = distance_transform_edt(f_) # return_indices=True
            self.dt_dy, self.dt_dx = np.gradient(self.d0)


    frames, wGc, K, Zs = loaddata1()
    fs = [Frame(f) for f in frames]
    f0,f1 = fs[0], fs[1]

    fig,(al,ar) = plt.subplots(1,2,num='p')
    al.imshow(f0.im)
    ar.imshow(f1.im)
    al.plot(f0.px, f0.py, 'r.' )
    ar.plot(f1.px, f1.py, 'b.' )

    f0.calcDT()
    al.imshow(f0.d0)

    err = sample(f0.d0, f1.px, f1.py)
    mask = ~np.isnan(err)
