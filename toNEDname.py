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
import re


def toNEDname(name, origin=None, twomass_id=None):
    """
    Convert a name string to NED-like (understandable) nomenclature

    Parameters
    ----------
    name : TYPE
        DESCRIPTION.
    origin : TYPE, optional
        DESCRIPTION. The default is None. Some replacements are only possible
        if the origin of the name is provided (CDS for NGC; B70 for LEDA)
    twomass_id : TYPE, optional.
        DESCRIPTION. The default is None. For 2MASS names, if the prefix is
        completely missing (as e.g., for 2MRS), provide the 2MASS ID here to
        generate the corresponding 2 MASS name as output

    # --- rename the objects to follow the NED convention:
    #     2MFGC *****
    #     2dFGRS TGN***Z*** --> 2dFGRS N***Z***
    #     2dFGRS TGS***Z*** --> 2dFGRS S***Z***
    #     6dFGS gJ --> 6dF J
    #     ESDO --> ESDO F
    #     ESO *-* --> ESO ***- G ***
    #     FRL    * --> FAIRALL ****
    #     IC ****
    #     IRAS ***** --> IRAS  ******
    #     NED: LEDA ****** --> LEDA *******
    #     LEDA *******
    #     MCG+**-**-*** --> MCG +**-**-***
    #     MGC *******
    #     Mrk    * --> MRK ****
    #     NGC ****
    #     Tol --> TOLOLO
    #     UGC *****
    #     2MRS: no prefix --> 2MASX J
    #     2MRS: 2MASX_J -->2MASX J
    #     2MRS: A --> 2MASX J
    #     2MR: g --> 2MASX J

    """


    nl = len(name)

    # --- prefix replacement:
    prefs = [["2dFGRS TGN", "2dFGRS N"],
             ["2dFGRS TGS", "2dFGRS S"],
             ["6dFGS gJ", "6dF J"],
             ["ESDO ", "ESDO F"],
             ["ESDO FF", "ESDO F"],
             ["FRL ", "FAIRALL "],
             ["IRAS ", "IRAS  "],
             ["IRAS   ", "IRAS  "],
             ["Mrk ", "MRK "],
             ["MCG+", "MCG +"],
             ["MCG-", "MCG -"],
             ["Tol ", "TOLOLO "],
             ["NGC  ", "NGC ", "CDS"],
             ["2MASXJ", "2MASX J"],
             ["LEDA", "LEDA ", "B70"]
             ]

    for p in prefs:
        if name.startswith(p[0]):

            # --- some name replacements are only valid for certain input sources
            if len(p) == 3 and origin is not None:
                if origin != p[2]:
                    break

            name = name.replace(p[0], p[1])
            break

    # --- ESO names are more complicated
    if name.startswith("ESO") and nl < 14:
        name = name.replace("ESO   ", "ESO 00")
        name = name.replace("ESO  ", "ESO 0")
        name = name.replace("-", "- G ")
        name = name.replace("G G", "G ")
        name = name.replace(" G IG", "IG ")
        name = name.replace(" G ?", " G?")

        nl = len(name)
        if nl == 12:
            name = name.replace("G ", "G 00")

        if nl == 13:
            name = name.replace("G ", "G 0")
            name = name.replace("G?", "G?0")


    # --- replace 2MRS names without prefix
    if name != "" and re.search('[a-zA-Z]+', name) == None:
        name = "2MASX J" + twomass_id


    # --- replace the 2MRS "_" with empty spaces which fixes most names
    if origin == "2MRS":
        name = name.replace("_", " ")

        if name.startswith("A") and not "M" in name:
            name = "2MASX J" + twomass_id

        if name.startswith("g"):
            name = "2MASX J" + twomass_id


    # -- replace empty spaces (as used by SIMBAD) with leading zeros
    zprefs = ["2MFGC ", "FAIRALL ", "IC ", "LEDA ", "MGC ", "MRK ", "NGC ",
              "UGC "]


    for z in zprefs:
        if name.startswith(z):
           for j in np.arange(5, 0, -1):
               name = name.replace(z + j * " ", z + j * "0")

           break


    # --- However, for LEDA objects there are leading zeros only up to 6 digits:
    if name.startswith("LEDA 0") and len(name) == 12:
        name = name.replace( "LEDA 0", "LEDA ")

    # --- For "MGC", we need to add two more zeroes to get the NED convention
    if name.startswith("MGC") and len(name) == 9:
        name = name.replace("MGC ", "MGC 00")


    # --- add zeros
#    zprefs = [["FAIRALL ", ],
#              ["IC ", ],
#              ["MRK ", ],
#              ["NGC ", ],
#              ["UGC ", ]
#             ]


    return(name)

