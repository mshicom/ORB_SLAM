#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 22:23:25 2016

@author: nubot
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import weave


def dt_2d(f):
    # f, q,p,Lambda = a,None,None, 1.0
    f_ = np.full_like(f, 1e10, 'f')
    f_[f!=0] = 0

    h,w = f.shape

    d = np.empty_like(f,'f')
    d_argx = np.empty_like(f,'i')
    d_argy = np.empty_like(f,'i')
    scode = r'''
        template <class T>
            inline T square(const T &x) { return x*x; };

        #define INF std::numeric_limits<float>::infinity()

        #define WIDTH  %(width)d
        #define HEIGHT %(height)d
        #define GET(im, x, y) (im[(x)+(y)*WIDTH])

        /* dt of 1d function using squared distance */
        static void dt(float *f, int n,
                       float *d, int *d_arg) {
          int *v = new int[n+1];
          float *z = new float[n+1];
          int k = 0;
          v[0] = 0;
          z[0] = -INF;
          z[1] = +INF;
          for (int q = 1; q <= n-1; q++) {
            float s  = ((f[q]+square(q))-(f[v[k]]+square(v[k])))/(2*q-2*v[k]);
            while (s <= z[k]) {
              k--;
              s  = ((f[q]+square(q))-(f[v[k]]+square(v[k])))/(2*q-2*v[k]);
            }
            k++;
            v[k] = q;
            z[k] = s;
            z[k+1] = +INF;
          }

          k = 0;
          for (int q = 0; q <= n-1; q++) {
            while (z[k+1] < q)
              k++;
            d[q] = square(q-v[k]) + f[v[k]];
            d_arg[q] = v[k];
          }

          delete [] v;
          delete [] z;
        }

        /* dt of 2d function using squared distance */
        static void dt(float *im, float *im_out, int *idx_out, int *idy_out) {

          float *f = new float[std::max(WIDTH, HEIGHT)];
          float *d = new float[std::max(WIDTH, HEIGHT)];
          int *d_id = new int[std::max(WIDTH, HEIGHT)];

          // transform along columns
          for (int x = 0; x < WIDTH; x++) {
            for (int y = 0; y < HEIGHT; y++) {
              f[y] = GET(im, x, y);
            }
            dt(f, HEIGHT, d, d_id);
            for (int y = 0; y < HEIGHT; y++) {
              GET(im_out, x, y) = d[y];
              GET(idy_out, x, y) = d_id[y];
            }
          }

          // transform along rows
          for (int y = 0; y < HEIGHT; y++) {
            for (int x = 0; x < WIDTH; x++) {
              f[x] = GET(im, x, y);
            }
            dt(f, WIDTH, d, d_id);
            for (int x = 0; x < WIDTH; x++) {
              GET(im_out, x, y) = d[x];
              GET(idx_out, x, y) = d_id[x];
            }
          }

          delete[] f;
          delete[] d;
          delete[] d_id;
        }
        ''' % {'height': h, 'width': w}
    code = r'''
        #define WIDTH  %(width)d
        #define HEIGHT %(height)d
        //std::raise(SIGINT);
        dt(f_,d,d_argx,d_argy);

        ''' % {'height': h, 'width': w}
    weave.inline(code,['d','d_argx','d_argy','f_',],
                 support_code=scode, headers=['<algorithm>','<cmath>','<vector>','<stdio.h>','<csignal>'],
                 compiler='gcc', extra_compile_args=['-std=gnu++11 -msse2 -O3'])
    return d, d_argx, d_argy
#%%
f = np.identity(100,'f')
d, idx, idy = dt_2d(f)
plt.imshow(d)
p = np.asarray(plt.ginput(1,-1)[0],'i')
ind = (p[1],p[0])
plt.plot([p[0], idx[ind]],
         [p[1], idy[ind]],'r')

import scipy.ndimage
f_ = np.full_like(f, 1e10, 'f')
f_[f!=0] = 0
d0,(idx,idy) = scipy.ndimage.distance_transform_edt(f_, return_indices=True)