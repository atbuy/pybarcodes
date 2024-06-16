from collections import namedtuple

from .codes import *
from .ean import *

__title__ = "pybarcodes"
__author__ = "atbuy"
__license__ = "MIT"
__copyright__ = "Copyright 2021-present atbuy"
__version__ = (0, 7, 5)

VersionInfo = namedtuple("VersionInfo", "major minor patch")

version_info = VersionInfo(*__version__)

SUPPORTED_BARCODES = ["EAN13", "EAN8", "EAN14", "JAN", "CODE39"]
