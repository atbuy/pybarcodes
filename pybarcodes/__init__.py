"""
pybarcodes
~~~~~~~~~~

A Python barcode generator

:copyright: (c) 2021-present Vitaman02
:license: MIT, see LICENSE for more details.
"""

__title__ = "pybarcodes"
__author__ = "Vitaman02"
__license__ = "MIT"
__copyright__ = "Copyright 2021-present Vitaman02"
__version__ = "0.3.2"


from collections import namedtuple


VersionInfo = namedtuple("VersionInfo", "major minor patch")

version_info = VersionInfo(major=2, minor=0, patch=0)