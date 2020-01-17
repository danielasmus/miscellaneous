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


import matplotlib as mpl
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'

from .ang_dist import ang_dist
from .combine_measurements import combine_measurements
from .compute_hist_dens import compute_hist_dens
from .coord_conversions import hours2deg, deg2hours
from .create_alpha_colmap import create_alpha_colmap
from .diffraction_limit import diffration_limit
from .effective_wlen import effective_wlen
from .flux_lum_conversions import lum2fnu, lum2flux, fnu2lum, flux2lum
from .flux_conversions import jansky2erg, erg2jansky, convert_flux, get_zp, mag2jansky, jansky2mag
from .freq_wave_conversions import micron2hertz, hertz2micron
from .synthphot import synthphot, synthphot_freq
from .timestamp import timestamp
from .toNEDname import toNEDname
import miscellaneous.wise as wise



