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




SPEED_OF_LIGHT = 2.99792458e8  # m/s


def micron2hertz(micron):
    """
    convert a wavelength in [micron] into a frequency in [Hz]
    """

    return(SPEED_OF_LIGHT / (1e-6 * micron))


def hertz2micron(hertz):
    """
    convert a frequency [Hz] into a wavelength [micron]
    """

    return(SPEED_OF_LIGHT/hertz*1e6)

