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


def combine_measurements(vals, errs=None, flags=None):

    """
    Combine different measurements for one quantity including upper (flag=1),
    lower (flag=2) limits and "not measured" (flag -1) with detections (flag=0)
    and return a weighted average and STDDEV or most constraining limit
    """

    warn = None

    if hasattr(vals, "__len__"):
        nm = len(vals)

        if nm == 1:
            vals = vals[0]

            if hasattr(errs, "__len__"):
                errs = errs[0]

            if hasattr(flags, "__len__"):
                flags = flags[0]

            return(vals, errs, flags, warn)

    else:
        return(vals, errs, flags, warn)

    vals = np.array(vals)

    if errs is None:
        errs = np.zeros(nm)

    if flags is None:
        flags = np.zeros(nm)

    errs = np.array(errs)
    flags = np.array(flags)

    # --- replace invalid (non-present errors with 0):
    idb = [ i for i, x in enumerate(errs) if not np.isfinite(errs[i])]

    if len(idb) > 0:
        warn = "WARNING: Non-valid errors encountered. Setting them to zero"
        errs[idb] = 0

    # --- check for strange values:
    idg = np.where((np.isfinite(vals)) & (flags >= -1) & (flags <= 2))[0]

    if len(idg) == 0:
        msg = "COMBINE_MEASUREMENTS: ERROR no valid measurement provided: "
        print(msg)
        print("vals: ", vals)
        print("errs: ", errs)
        print("flags: ", flags)

        return(0, 0, -1, msg)

    else:
        vals = vals[idg]
        errs = errs[idg]
        flags = flags[idg]

    # --- detections
    idd = np.where(flags == 0)[0]
    nd = len(idd)

    # --- upper limits
    idu = np.where(flags == 1)[0]
    nu = len(idu)

    # --- lower limits
    idl = np.where(flags == 2)[0]
    nl = len(idl)

    # --- not measured
    idn = np.where(flags == -1)[0]
    nn = len(idn)

    # --- Cases:
    #   1. all not measured: retun 0,0,-1
    #   2. only upper limits: return lowest value, 0, 1
    #   3. only lower limits: return higher value, 0, 2
    #   4. only detection & not measured: return mean, std, 0
    #   5. detection & upper limit: return mean, std, warning if higher than upper limit
    #   6. detection & lower limit: return mean, std, warning if lower than lower limit


    minval = None
    maxval = None

    # --- 1. all not measured: retun 0,0,-1
    if nn == nm:
        return(0, 0, -1, None)

    # --- In case of upper limits find the most constraining (lowest)
    if nu > 0:
        minval = np.min(vals[idu])

    # --- In case of lower limits find the most constraining (highest)
    if nl > 0:
        maxval = np.max(vals[idl])

    #  --- In case there is at least on detecten:
    if nd > 0:

        # --- If only one detection, nothing to compute
        if nd == 1:
            val = vals[idd[0]]
            err = errs[idd[0]]

        # --- if there are several, compute the weighted mean and STDDEV
        else:
            if np.min(errs[idd]) == 0:
                weights=np.ones(nd)

            else:
                weights = 1.0/errs[idd]**2

            val = np.average(vals[idd], weights=weights)
            err = np.sqrt(np.average((vals[idd]-val)**2, weights=weights))


        # --- 5. detection & upper limit: return mean, std, warning if higher than upper limit
        if nu > 0:
            if val-err > minval:
                warn = ("WARNING: weighted mean of detection larger than upper limit: "
                        + "{:.3E}".format(val) + ' +/- '
                        + "{:.3E}".format(err) + ' > '
                        + "{:.3E}".format(minval))

        # --- 6. detection & lower limit: return mean, std, warning if lower than lower limit
        if nl > 0:
            if val+err < maxval:
                warn = ("WARNING: weighted mean of detection smaller than lower limit: "
                        + "{:.3E}".format(val) + '+/- '
                        + "{:.3E}".format(err) + ' < '
                        + "{:.3E}".format(maxval))

        return(val, err, 0, warn)

    # --- if only upper limits return the lowest
    elif nu > 0:
        return(minval, 0, 1, None)

    # --- if only lower limits return the highest
    elif nl > 0:
        return(maxval, 0, 2, None)



