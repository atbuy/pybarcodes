from setuptools import setup
from pybarcodes.__init__ import __version__


requirements = [
    "Pillow>=8.0.1",
    "numpydoc==1.1.0"
]


readme = """
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


"""


setup(
    name="pybarcodes",
    author="Vitaman02",
    url="https://github.com/Vitaman02/pybarcodes",
    project_urls={},
    version=__version__,
    packages=["pybarcodes"],
    license="MIT",
    description="A Python barcode generator",
    long_description=readme,
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.6.0",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ]

)
