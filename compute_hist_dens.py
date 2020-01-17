#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = "1.0.0"

"""
HISTORY:
    - 2020-01-15: created by Daniel Asmus


NOTES:
    -

TO-DO:
    -
"""


import numpy as np
from scipy.interpolate import interpn


def compute_hist_dens(x,y, nbins):

    """
    Little helper routine to make binned density plots of 2D distributions of
    points.
    Compute a z-value for a 2D distribution of points given by x,y coordinates
    that corresponds to the density of points in each position. For this, a
    simple 2D histogram with nbins over the total x,y distirbution is used.
    """

    #--- do a simple 2D histogram
    hd, x_e, y_e = np.histogram2d(x, y, bins=nbins)
    z = interpn(( 0.5*(x_e[1:] + x_e[:-1]), 0.5*(y_e[1:]+y_e[:-1]) ), hd,
                np.vstack([x,y]).T, method="splinef2d", bounds_error=False )

    # --- Sort the points by density, so that the densest points are plotted last
    idx = z.argsort()
    x, y, z = x[idx], y[idx], z[idx]

    return([x,y,z])

