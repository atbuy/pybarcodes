from collections import namedtuple

from pybarcodes.codes import CODE39, Code  # noqa: F401
from pybarcodes.ean import EAN, EAN8, EAN13, EAN14, JAN, Size, Weights  # noqa: F401

__title__ = "pybarcodes"
__author__ = "atbuy"
__license__ = "MIT"
__copyright__ = "Copyright 2021-present atbuy"
__version__ = (1, 0, 0)

VersionInfo = namedtuple("VersionInfo", "major minor patch")

version_info = VersionInfo(*__version__)

SUPPORTED_BARCODES = ["EAN13", "EAN8", "EAN14", "JAN", "CODE39"]
