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


SPEED_OF_LIGHT = 2.99792458e8  # m/s

def lum2fnu(lum, dist, wlen, log_fnu=False, log_dist=False, log_lum=True,
            fnu_unit='Jy', log_wlen=False):
    """
    Convert a luminosity into flux density in Jy (or in 'mJy') for a given
    distance in Mpc and wavelength in [micron]

    """


    if log_wlen == False:
        wlen = np.log10(wlen)

    freq = np.log10(2.99792e8) - wlen + 6

    if log_dist == False:
        dist = np.log10(dist)


    if log_lum == False:
        lum = np.log10(lum)

    nufnu  = lum - np.log10(4.0 * np.pi) - 2*dist - 2*np.log10(3.086e24)

    fnu = nufnu - freq + 23

    if fnu_unit == 'mJy':
        fnu = fnu - 3

    if log_fnu == False:
        fnu = 10.0**fnu

    return(fnu)



def lum2flux(lum, dist, log_flux=False, log_dist=False, log_lum=True,
            flux_unit='erg/s/cm^2'):
    """
    Convert a given luminosity into flux for a given distance in [Mpc]
    """


    if log_dist == False:
        dist = np.log10(dist)

    if log_lum == False:
        lum = np.log10(lum)

    flux  = lum - np.log10(4.0 * np.pi) - 2*dist - 2*np.log10(3.086e24)

    if flux_unit == 'W/m^2':
        flux = flux + 3
    elif flux_unit != 'erg/s/cm^2':
        print("MISC.FLUX2LUM: ERROR: flux_unit not understood: "+ flux_unit +
              " Return -1! ")
        return(-1)

    if log_flux == False:
        flux = 10.0**flux

    return(flux)



def fnu2lum(fnu, dist, wlen, log_fnu=False, log_dist=False, log_lum=True,
            fnu_unit='Jy', log_wlen=False):
    """
    Convert a flux density in Jy (or in 'mJy') into luminosity for a given
    distance in Mpc and wavelength in [micron]
    """


    if log_wlen == False:
        wlen = np.log10(wlen)

    freq = np.log10(2.99792e8) - wlen + 6

    if log_fnu == False:
        fnu = np.log10(fnu)

    if fnu_unit == 'mJy':
        fnu = fnu - 3

    nufnu = fnu + freq - 23

    if log_dist == False:
        dist = np.log10(dist)

    lum = nufnu + np.log10(4.0 * np.pi) + 2*dist + 2*np.log10(3.086e24)

    if log_lum == False:

        lum = 10.0**lum

    return(lum)



def flux2lum(flux, dist, log_flux=False, log_dist=False, log_lum=True,
            flux_unit='erg/s/cm^2', log_wlen=False):
    """
    Convert a given flux into luminosity for a given distance in [Mpc]
    """

    if log_flux == False:
        flux = np.log10(flux)

    if flux_unit == 'W/m^2':
        flux = flux + 3
    elif flux_unit != 'erg/s/cm^2':
        print("MISC.FLUX2LUM: ERROR: flux_unit not understood: "+ flux_unit +
              " Return -1! ")
        return(-1)

    if log_dist == False:
        dist = np.log10(dist)

    lum = flux + np.log10(4.0 * np.pi) + 2*dist + 2*np.log10(3.086e24)

    if log_lum == False:

        lum = 10.0**lum

    return(lum)

