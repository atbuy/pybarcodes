"""
pybarcodes
~~~~~~~~~~

A Python barcode generator

:copyright: (c) 2021-present Vitaman02
:license: MIT, see LICENSE for more details.
"""

from collections import namedtuple
from .ean import *
from .codes import *

__title__ = "pybarcodes"
__author__ = "Vitaman02"
__license__ = "MIT"
__copyright__ = "Copyright 2021-present Vitaman02"
__version__ = "0.7.2"

VersionInfo = namedtuple("VersionInfo", "major minor patch")

version_info = VersionInfo(*map(int, __version__.split(".")))

SUPPORTED_BARCODES = ["EAN13", "EAN8", "EAN14", "JAN", "CODE39"]
