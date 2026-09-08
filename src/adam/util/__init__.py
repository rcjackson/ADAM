"""
===============================================
ADAM Utility Functions (:mod:`adam.util`)
=============================================== 

.. currentmodule:: adam.util

This module contains utility functions for the ADAM package.

.. autosummary::
    :toctree: generated/

    azimuth_point
    azimuth_from_ellipse
    aeqd_to_lonlat
"""

from .geodesy import aeqd_to_lonlat
from .instrument_steering import azimuth_from_ellipse, azimuth_point
