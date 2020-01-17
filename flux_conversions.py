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

def jansky2erg(fnu, wlen):
    """
    convert a flux density in [Jy] into a flux [erg/s/cm^2] for a given
    wavelength in [micron]

    """

    # 1 Jansky = 1.d-23 erg/s/cm^2 / Hz

    freq = SPEED_OF_LIGHT / (1e-6 * wlen)
    nufnu = fnu * 1.0e-23 * freq

    return(nufnu)


def erg2jansky(nufnu, wlen):
    """
    convert a flux [erg/s/cm^2] into a flux density in [Jy] for a given
    wavelength in [micron]
    """

    # 1 Jansky = 1.d-23 erg/s/cm^2 / Hz

    freq = SPEED_OF_LIGHT / (1e-6 * wlen)
    fnu = nufnu / 1.0e-23 / freq

    return(fnu)


def get_zp(filt):
    """
    Return the approximate zero point in Jy in Vega for a given filter name
    (slight differences between different instruments are ignored).
    Currently included are:
        - 2MASS: 'J', 'H', 'K',
        - WISE: 'W1', 'W2', 'W3', 'W4'
        - NACO: 'Lp', 'Mp', ISAAC: 'M_NB', 'L'
        - VISIR/T-ReCs: 'N', 'Np', 'Q'
    """

    wise_zps = np.array([309.540, 171.787, 31.674, 8.363])  # Jy
    tmass_zps = np.array([1594.0, 1024.0, 666.8]) # Jy
    L_zp = 247.2    # ISAAC
    M_NB_zp = 164.5    # ISAAC
    Lp_zp = 244.2   # NACO
    Mp_zp = 159.7   # NACO
    N_zp = 37.0  # Michelle/T-ReCs N
    Np_zp = 30.0   # approximate 12um
    Q_zp = 10.0  # median of VISIR/Michelle/T-ReCs

    if filt == "J":
        zp_Jy = tmass_zps[0]
    elif filt == "H":
        zp_Jy = tmass_zps[1]
    elif filt == "K" or filt == "Ks":
        zp_Jy = tmass_zps[3]
    elif filt == "W1":
        zp_Jy = wise_zps[0]
    elif filt == "W2":
        zp_Jy = wise_zps[1]
    elif filt == "W3":
        zp_Jy = wise_zps[2]
    elif filt == "W4":
        zp_Jy = wise_zps[3]
    elif filt == "L":
        zp_Jy = L_zp
    elif filt == "M" or filt == "M_NB":
        zp_Jy = M_NB_zp
    elif filt == "Lp":
        zp_Jy = Lp_zp
    elif filt == "Mp":
        zp_Jy = Mp_zp
    elif filt == "N":
        zp_Jy = N_zp
    elif filt == "Np":
        zp_Jy = Np_zp
    elif filt == "Q":
        zp_Jy = Q_zp

    return(zp_Jy)



def mag2jansky(mag, zp_Jy=None, filt=None):

    """
    convert a magnitude to a flux density either by a given zeropoint in Jy
    or a filter name
    """
    if filt is not None:
        zp_Jy = get_zp(filt)

    return(zp_Jy * 10 ** (-mag/2.5))



def jansky2mag(jy, zp_Jy=None, filt=None):

    """
    convert a flux density to a magnitude for either given zeropoint in Jy
    or a filte rname
    """
    if filt is not None:
        zp_Jy = get_zp(filt)

    return(-2.5 * np.log10(jy/zp_Jy))



def convert_flux(flux, inunit, outunit, inlog=False, outlog=False,
                 wlen=None, freq=None, wunit="micron",
                 wlog=False, flog=False):

    """
    Convert a flux or flux density into a flux or flux density of a different
    unit.
    allowed input/output units are 'mJy', 'Jy', 'W/m^2' or erg/s/cm^2' and for
    wavelength either 'micron', 'nm', 'angstr', 'cm', 'm'. For frequency, the
    unit has to be 'Hertz'
    """

    if inlog == True:
        flux = 10.0**flux

    # --- simple cases
    if inunit == "mJy" and outunit == "Jy":
        flux = flux * 1e-3

    elif inunit == "Jy" and outunit == "mJy":
        flux = flux * 1e-3

    elif inunit == "W/m^2" and outunit == "erg/s/cm^2":
        flux = flux * 1e3

    elif inunit == "erg/s/cm^2" and outunit == "W/m^2":
        flux = flux * 1e-3

    # --- ok now the cross-overs
    else:

        if freq is None:
            if wlog:
                wlen == 10.0**wlen

            if wunit == "micron":
                wlen = 1e-6 * wlen
            elif wunit == "nm":
                wlen = 1e-9 * wlen
            elif wunit == "angstr":
                wlen = 1e-10 * wlen
            elif wunit == "cm":
                wlen = 1e-2 * wlen

            freq = SPEED_OF_LIGHT/wlen
        else:
            if flog:
                freq = 10.0**freq
#            if funit is not "hertz":
#                print("CONVERT_FLUX: ERROR not implemented frequency unit supplied! Returning -1")
#                return(-1)

        # --- now convert to nufnu with W/m^2 or Jy
        if inunit == "mJy":
            flux = flux * 1.0e-29 * freq
        elif inunit == "Jy":
            flux = flux * 1.0e-26 * freq
        elif inunit == "W/m^2":
            flux = flux * 1.0e26 / freq
        elif inunit == "erg/s/cm^2":
            flux = flux * 1.0e23 / freq

        if outunit == "erg/s/cm^2" or outunit == "mJy":
            flux = flux * 1e3

    if outlog == True:
        flux == np.log10(flux)

    return(flux)

