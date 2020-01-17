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



from scipy.integrate import simps


def effective_wlen(fwlen, ftrans, alpha=0):
    """
    Compute the effective wavelength for a given filter transfer function and a
    reference spectrum with the power law slope alpha

    """

    eff_wlen = (simps(ftrans*fwlen*fwlen**(-1*alpha-1),fwlen)
                 / simps(ftrans*fwlen**(-1*alpha-1),fwlen))

    return(eff_wlen)