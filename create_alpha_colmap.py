#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = "1.1.0"

"""
HISTORY:
    - 2020-01-15: created by Daniel Asmus
    - 2020-01-17: option for different scaling added


NOTES:
    -

TO-DO:
    -
"""


import numpy as np
import matplotlib as mpl
from matplotlib.colors import colorConverter


def create_alpha_colmap(mincol='black',maxcol='black', minalpha=0, maxalpha=1,
                        scale="lin"):
    """
    create a matplotlib colormap with a gradient in alpha and/or color

    Parameters
    ----------
    mincol : TYPE, optional
        DESCRIPTION. The default is 'black'.
    maxcol : TYPE, optional
        DESCRIPTION. The default is 'black'.
    minalpha : TYPE, optional
        DESCRIPTION. The default is 0.
    maxalpha : TYPE, optional
        DESCRIPTION. The default is 1.
    scale : TYPE, optional
        DESCRIPTION. The default is "lin". Other options are "asinh", "log",
        "square", "cubic", "exp"

    Returns
    -------
    None.

    """


    # generate the colors for your colormap
    color1 = colorConverter.to_rgba(mincol)
    color2 = colorConverter.to_rgba(maxcol)

    # make the colormap
    cmap = mpl.colors.LinearSegmentedColormap.from_list('my_cmap2',[color1,color2],256)
    cmap._init() # create the _lut array, with rgba values

    # create your alpha array and fill the colormap with them.
    # here it is progressive, but you can create whathever you want
    if scale == "lin" or scale == "linear":
        alphas = np.linspace(minalpha, maxalpha, cmap.N+3)
    elif scale == "asinh":
        alphas = np.arcsinh(np.linspace(0, 1, cmap.N+3))/np.arcsinh(1) * (maxalpha-minalpha) + minalpha
    elif scale == "log":
        alphas = 0.1 * np.logspace(0, 1, cmap.N+3) * (maxalpha-minalpha) + minalpha
    elif scale == "square":
        alphas = np.linspace(0, 1, cmap.N+3)**2 * (maxalpha-minalpha) + minalpha
    elif scale == "sqrt":
        alphas = np.linspace(0, 1, cmap.N+3)**0.5 * (maxalpha-minalpha) + minalpha
    elif scale == "cubic":
        alphas = np.linspace(0, 1, cmap.N+3)**3 * (maxalpha-minalpha) + minalpha
    elif scale == "exp":
        alphas = 0.1*10.0**np.linspace(0, 1, cmap.N+3) * (maxalpha-minalpha) + minalpha

    cmap._lut[:,-1] = alphas

    return(cmap)


