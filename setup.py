from pathlib import Path

from setuptools import find_packages, setup

cwd = Path(__file__).parent
readme_path = cwd.joinpath("README.rst")

requirements = [
    "Pillow>=8.0.1",
    "numpydoc>=1.1.0",
]

readme = ""
with open(readme_path) as file:
    readme = file.read()

setup(
    name="pybarcodes",
    author="atbuy",
    url="https://github.com/atbuy/pybarcodes",
    project_urls={},
    version="0.7.3",
    packages=find_packages(),
    license="MIT",
    description="A Python barcode generator",
    long_description=readme,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.8.0",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
)
