pybarcodes
==========

.. image:: https://readthedocs.org/projects/pybarcodes/badge/?version=latest
    :target: https://pybarcodes.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/pybarcodes.svg
    :target: https://pypi.python.org/pypi/pybarcodes
    :alt: PyPI version info

.. image:: https://img.shields.io/pypi/pyversions/pybarcodes.svg
    :target: https://pypi.python.org/pypi/pybarcodes
    :alt: PyPI supported Python versions

This is a python package to create and read barcodes


Installing
-----------

**Python 3.6.0 or higher is required**

To install the library you can run the following command:

.. code:: sh

    # Linux/MacOS
    python3 -m pip install --upgrade pybarcodes

    # Windows
    py -3 -m pip install --upgrade pybarcodes


Quick Example
--------------

.. code:: py

    from pybarcodes.ean import EAN13

    CODE = "012345678905"
    barcode = EAN13(CODE)
    barcode.show()


This is all the code you need to generate a barcode.

Output Image:

.. image:: https://i.imgur.com/mlWpuqW.png
    :target: https://i.imgur.com/mlWpuqW.png
    :alt: Image of Barcode


Links
------

- `Documentation <https://pybarcodes.readthedocs.io/en/latest/index.html>`_


