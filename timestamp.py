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

import datetime
import time

def timestamp():
    """
    return a handy string with the current time
    """

    return(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))

