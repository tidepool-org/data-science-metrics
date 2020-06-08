#!/usr/bin/env python3

import setuptools
import sys


# validate python version
if sys.version_info < (3, 6):
    sys.exit("Sorry, Python < 3.6 is not supported")

# %% START OF SETUP
with open("README.md", "r") as fh:
    long_description = fh.read()

version_string = "v0.1.1"

setuptools.setup(
    name="Tidepool Data Science Metrics",
    version=version_string,
    author="Russ Wilson and Ed Nykaza",
    author_email="ed@tidepool.org",
    description="Set of functions to produce common metrics used in Data Science at Tidepool.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tidepool-org/data-science-metrics",
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    download_url=(
        "https://github.com/tidepool-org/data-science-metrics/tarball/" + version_string
    ),
    setup_requires=["wheel"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=["numpy>=1.18.1", "pandas>=1.0.1",],
)
