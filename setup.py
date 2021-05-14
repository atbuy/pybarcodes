from setuptools import setup
from pycodes.__init__ import __version__


requirements = []
with open("requirements.txt") as file:
    requirements = file.readlines()


readme = ""
with open("README.md") as file:
    readme = file.read()


setup(
    name="pycodes",
    author="Vitaman02",
    url="https://github.com/Vitaman02/Barcodes",
    project_urls=[],
    version=__version__,
    packages=["pycodes"],
    license="MIT",
    description="A Python barcode generator",
    long_description=readme,
    long_description_content_type="text/x-rst",
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
