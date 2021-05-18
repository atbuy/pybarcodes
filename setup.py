import os
from setuptools import setup, find_packages


this_dir = os.path.abspath(os.path.dirname(__file__))


requirements = []
with open(os.path.join(this_dir, "requirements.txt")) as file:
    requirements = file.read().splitlines()


readme = ""
with open(os.path.join(this_dir, "README.rst")) as file:
    readme = file.read()


setup(
    name="pybarcodes",
    author="Vitaman02",
    url="https://github.com/Vitaman02/pybarcodes",
    project_urls={},
    version="0.6.5",
    packages=find_packages(),
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
