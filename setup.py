from pathlib import Path

from setuptools import find_packages, setup

cwd = Path(__file__).parent
readme_path = cwd.joinpath("README.rst")

requirements = [
    "Pillow>=8,<12",
]

doc_requirements = [
    "numpydoc>=1.1.0",
]

test_requirements = [
    "pytest==8.2.2",
    "pytest-cov==5.0.0",
]

extras = {"test": test_requirements, "doc": doc_requirements}

readme = ""
with open(readme_path) as file:
    readme = file.read()

setup(
    name="pybarcodes",
    author="atbuy",
    url="https://github.com/atbuy/pybarcodes",
    project_urls={},
    version="1.0.0",
    packages=find_packages(),
    license="MIT",
    description="A Python barcode generator",
    long_description=readme,
    long_description_content_type="text/x-rst",
    package_data={"": ["fonts/*.ttf"]},
    include_package_data=True,
    install_requires=requirements,
    extras_require=extras,
    python_requires=">=3.9",
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
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
)
