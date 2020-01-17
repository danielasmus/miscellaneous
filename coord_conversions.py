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


from astropy import units as u
from astropy.coordinates import SkyCoord

def hours2deg(rastr,decstr):
    """
    Converts sexagesimal coordinates (given as string) into degrees
    """

    c = SkyCoord(rastr, decstr, unit=(u.hourangle, u.deg))

    return(c.ra.deg, c.dec.deg)


def deg2hours(radeg,decdeg):
    """
    Converts coordinates given in degrees into sexagesimal (returns strings)
    """

    c = SkyCoord(radeg, decdeg, unit=(u.deg, u.deg))

    rastr = c.to_string(style='hmsdms').split()[0]
    decstr = c.to_string(style='hmsdms').split()[1]

    return(rastr, decstr)



