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


def diffration_limit(diam, wlen):
    """
    compute the diffraction limit in [arcsec] for telescope diameter [m] and
    wavelength [um]
    """
    diflim = np.arcsin(1.028*wlen*0.000001/diam)*206264.806247  # arcsec

    return(diflim)
