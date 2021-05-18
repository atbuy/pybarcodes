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
You can create file-like objects, text files and images from just a barcode number.
Image generation is fast so it can be used to create images in bulk.


Supported Barcode Types
------------------------

- EAN13
- EAN8
- EAN14
- JAN

More types will soon be supported.
PRs are welcome :)


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

You can see what barcodes are supported

.. code:: py

    >>> import pybarcodes
    >>> pybarcodes.SUPPORTED_BARCODES
    ['EAN13', 'EAN8', 'EAN14', 'JAN']



And you can use this to view the barcode that was generated:

.. code:: py

    from pybarcodes import EAN13

    CODE = "012345678905"
    barcode = EAN13(CODE)
    barcode.show()

This is pretty much all the code you need to generate a barcode.


Saving an image of the barcode is pretty straightforward.

.. code:: py

    from pybarcodes import EAN14

    barcode = EAN14("40700719670720")

    # Saves the image in PNG format
    barcode.save("myimage.png")

    # You can also resize it.
    barcode.save("myimage2.png", size=(100000, 1000000))




EAN13 output from example 2:

.. image:: https://i.imgur.com/wd7jyIx.png
    :target: https://i.imgur.com/wd7jyIx.png
    :alt: Image of Barcode


Links
------

- `Documentation <https://pybarcodes.readthedocs.io/en/latest/index.html>`_

