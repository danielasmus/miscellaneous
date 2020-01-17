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


import numpy as np
from scipy.integrate import simps

from .freq_wave_conversions import micron2hertz as _micron2hertz


def synthphot(wavelen, fluxden, fwlen, ftrans, ref_wlen,
              ignore_incomplete=False,
              acceptable_hole=0.7, alpha=-2):
    """
    Perform synthetic photometry on a spectrum wavelen, fluxden for a given
    filter transfer function and reference wavelength

    Parameters
    ----------
    wavelen : TYPE float array
        DESCRIPTION. Wavelength array of the spectrum
    fluxden : TYPE float array
        DESCRIPTION. Flux density, fnu, array of the spectrum
    fwlen : TYPE float array
        DESCRIPTION. filter transfer function wavelength array
    ftrans : TYPE float array
        DESCRIPTION. filter transfer function transmission
    ref_wlen : TYPE float
        DESCRIPTION. Reference wavelength (should normally be the effective
        wavelength of the filter)
    ignore_incomplete : TYPE bool, optional
        DESCRIPTION. The default is False. Flag to allow the spectrum not
        covering the whole filter transfer function
    acceptable_hole : TYPE float, optional
        DESCRIPTION. The default is 0.7. Maximum allowed spacing between two
        points in the spectrum in wavelength direction (in input units)
    alpha : TYPE int, optional
        DESCRIPTION. The default is -2. Power law index of the reference
        spectrum snu = fwlen**(-1*alpha)

    Returns
    -------
    float: synthetic flux density in input units

    """

   # ---- first exclude invalid data points
    id = wavelen != 0
    wlen = wavelen[id]
    inten = fluxden[id]

    # --- sort wavelength
    id = np.argsort(wlen)
    wlen = wlen[id]
    inten = inten[id]
    npix = len(wlen)

    # --- test whether spectrum covers filter curve without any holes
    if ignore_incomplete is False:

        if ((np.nanmin(fwlen) < np.nanmin(wlen))
            or (np.nanmax(fwlen) > np.nanmax(wlen))):

            print("ERROR: spectrum not covering whole filter curve. Abort...")
            return(-1)

        wdiffs = np.zeros(npix)

        for i in np.arange(1, npix):
            if (wlen[i] >= np.nanmin(fwlen) and wlen[i] <= np.nanmax(fwlen)):
                wdiffs[i] = wlen[i] - wlen[i-1]

        if (np.nanmax(wdiffs) > acceptable_hole):

            print("ERROR: spectrum has a hole larger than allowed. Abort...")
            ids = np.nanargmax(wdiffs)
            print(wdiffs[ids], wlen[ids])
            return(-1)


    # --- normalize the filter function for the overlapping region
    id = np.where((fwlen >= wlen[0]) & (fwlen <= wlen[npix-1]))[0]
    ftrans = ftrans[id]
    fwlen = fwlen[id]

    n = len(fwlen)

    snu = fwlen**(-1*alpha)
    snu_ref = ref_wlen**(-1*alpha)

    a = simps(ftrans/fwlen*snu, fwlen)

    ftrans = ftrans / a

    # --- apply the filter to the spectrum ---
    id = (wlen >= fwlen[0]) & (wlen <= fwlen[n-1])

    wlen = wlen[id]
    inten = inten[id]

    npix = len(wlen)

    # eff_wlen = effect_wavelen(fwlen, ftrans, alpha=alpha)

    ftrans = np.interp(wlen, fwlen, ftrans)

    # f = interp1d(fwlen,ftrans,kind='cubic')
    # ftrans = f(wlen)

    # inten = np.interp(fwlen, wlen, inten)

    # synflux = simps(inten*ftrans/fwlen,fwlen) * snu_ref
    synflux = simps(inten*ftrans/wlen,wlen) * snu_ref

    return(synflux)


#%%
def synthphot_freq(wavelen, fluxden, fwlen, ftrans, ref_wlen,
              ignore_incomplete=False,
              acceptable_hole=0.7, alpha=-2):

    """
    Alternative: Perform synthetic photometry on a spectrum wavelen, fluxden for a given
    filter transfer function and reference wavelength in frequency space

    Parameters
    ----------
    wavelen : TYPE float array
        DESCRIPTION. Wavelength array of the spectrum
    fluxden : TYPE float array
        DESCRIPTION. Flux density, fnu, array of the spectrum
    fwlen : TYPE float array
        DESCRIPTION. filter transfer function wavelength array
    ftrans : TYPE float array
        DESCRIPTION. filter transfer function transmission
    ref_wlen : TYPE float
        DESCRIPTION. Reference wavelength (should normally be the effective
        wavelength of the filter)
    ignore_incomplete : TYPE bool, optional
        DESCRIPTION. The default is False. Flag to allow the spectrum not
        covering the whole filter transfer function
    acceptable_hole : TYPE float, optional
        DESCRIPTION. The default is 0.7. Maximum allowed spacing between two
        points in the spectrum in wavelength direction (in input units)
    alpha : TYPE int, optional
        DESCRIPTION. The default is -2. Power law index of the reference
        spectrum snu = fwlen**(-1*alpha)

    Returns
    -------
    float: synthetic flux density in input units

    """


    # ---- first exclude invalid data points
    id = wavelen != 0
    wlen = wavelen[id]
    inten = fluxden[id]

     # --- convert to frequency space
    freq = _micron2hertz(wlen)
    ffreq = _micron2hertz(fwlen)

    # --- sort wavelength
    id = np.argsort(freq)
    freq = freq[id]
    inten = inten[id]
    npix = len(wlen)

    id = np.argsort(ffreq)
    ffreq = ffreq[id]
    ftrans = ftrans[id]

    # --- test whether spectrum covers filter curve without any holes
    if ignore_incomplete is False:

        if ((np.nanmin(fwlen) < np.nanmin(wlen))
            or (np.nanmax(fwlen) > np.nanmax(wlen))):

            print("ERROR: spectrum not covering whole filter curve. Abort...")
            return(-1)

        wdiffs = np.zeros(npix)

        for i in np.arange(1, npix):
            if (wlen[i] >= np.nanmin(fwlen) and wlen[i] <= np.nanmax(fwlen)):
                wdiffs[i] = wlen[i] - wlen[i-1]

        if (np.nanmax(wdiffs) > acceptable_hole):

            print("ERROR: spectrum has a hole larger than allowed. Abort...")
            return(-1)


    # --- normalize the filter function for the overlapping region
    id = (ffreq >= freq[0]) & (ffreq <= freq[npix-1])
    ftrans = ftrans[id]
    ffreq = ffreq[id]

    n = len(ffreq)

    snu = ffreq**(alpha)
    ref_freq = _micron2hertz(ref_wlen)
    snu_ref = ref_freq**(alpha)

    a = simps(ftrans/ffreq*snu, ffreq)

    ftrans = ftrans / a

    # --- apply the filter to the spectrum ---
    id = (freq >= ffreq[0]) & (freq <= ffreq[n-1])

    freq = freq[id]
    inten = inten[id]

    npix = len(freq)

    # eff_freq = effect_wavelen(ffreq, ftrans, alpha=alpha)

    ftrans = np.interp(freq, ffreq, ftrans)

    synflux = simps(inten*ftrans/freq,freq) * snu_ref

    return(synflux)

