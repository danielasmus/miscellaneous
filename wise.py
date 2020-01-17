#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = "1.0.0"

"""
HISTORY:
    - 2020-01-17: created by Daniel Asmus


NOTES:
    -

TO-DO:
    -
"""


import numpy as _np

wlens = _np.array([3.3526, 4.6028, 11.5608, 22.8])
hwidths = _np.array([0.663, 1.042, 5.506, 4.102]) * 0.5


# %%
def mag2jansky(mags, merrs=None, cc=False, w4cor=True):

    """
    Convert the WISE magnitudes into flux densities using the conversion
    relations and color corrections given in the documentation:
    http://wise2.ipac.caltech.edu/docs/release/allsky/expsup/sec4_4h.html#FluxCC
    """

    mags = _np.array(mags, dtype=float)

    # --- first calculate the colors
    W1W2 = mags[0] - mags[1]
    W2W3 = mags[1] - mags[2]
    W3W4 = mags[2] - mags[3]

    # --- use the color correction table given in Wright et al. 2010
    fc1 = _np.array([1.0283, 1.0084, 0.9961, 0.9907, 0.9921, 1.0, 1.0142, 1.0347])
    fc2 = _np.array([1.0206, 1.0066, 0.9976, 0.9935, 0.9943, 1.0, 1.1081, 1.2687])
    fc3 = _np.array([1.1344, 1.0088, 0.9292, 0.9169, 0.9373, 1.0, 1.1081, 1.2687])
    fc4 = _np.array([1.0142, 1.0013, 0.9934, 0.9905, 0.9926, 1.0, 1.0130, 1.0319])

    col1 = _np.array([-0.404, -0.0538, 0.2939, 0.6393, 0.9828, 1.3246, 1.6649, 2.0041])
    col2 = _np.array([-0.9624, -0.0748, 0.8575, 1.8357, 2.8586, 3.9225, 5.0223, 6.1524])
    col3 = _np.array([-0.8684, -0.0519, 0.72, 1.4458, 2.1272, 2.7680, 3.3734, 39495])

    # --- determine the corrections based on the actual color and interpolation
    #     of the above table
    if cc is True:

        cc1 = _np.interp(W1W2, col1, fc1)

        cc2 = _np.mean([_np.interp(W1W2, col1, fc2), _np.interp(W2W3, col2, fc2)])

        cc3 = _np.mean([_np.interp(W2W3, col2, fc3), _np.interp(W3W4, col3, fc3)])

        cc4 = _np.interp(W3W4, col3, fc4)

    #print(cc1,cc2,cc3,cc4)

        cc = _np.array([cc1, cc2, cc3, cc4])

        # --- zero points
        zps = _np.array([306.682, 170.663, 29.045, 8.284])  # Jy

        fluxes = zps / cc * 10 ** (-mags/2.5)

    else:

        # --- zero points
        zps = _np.array([309.540, 171.787, 31.674, 8.363])  # Jy
        cc = 1

        fluxes = zps * 10 ** (-mags/2.5)



    # --- additional flux correction in W4 for very red sources (alpha >=1):
    if (W3W4 >= 2.1272) and (w4cor is True):
        fluxes[3] = 0.9 * fluxes[3]

    # --- if the magnitude errors are provide compute the flux errors using the
    #     maximum of the upper and lower error
    if merrs is not None:

        merrs = _np.array(merrs, dtype=float)

        # --- check for non-detections and set the error very large
        nondet = _np.array(_np.where(_np.isnan(merrs)))[0]

        if sum(nondet) > 0:
            #print(nondet)
            merrs[nondet] = mags[nondet]

        uf = zps / cc * 10 ** (-(mags-merrs)/2.5)
        lf = zps / cc * 10 ** (-(mags+merrs)/2.5)

        errors = _np.max([uf-fluxes, fluxes-lf],axis=0)

        return(fluxes,errors)

    else:
       return(fluxes)

