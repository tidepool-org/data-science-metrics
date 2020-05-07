#!/usr/bin/env python3

import setuptools
import os
import glob
import shutil
import sys


# validate python version
if sys.version_info < (3, 6):
    sys.exit("Sorry, Python < 3.6 is not supported")

# %% START OF SETUP
with open("README.md", "r") as fh:
    long_description = fh.read()

version_string = "v0.0.5"

setuptools.setup(
    name="Tidepool Data Science Metrics",
    version=version_string,
    author="Russ Wilson",
    author_email="russ@tidepool.org",
    description="Set of functions to produce common metrics used in Data Science at Tidepool.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tidepool-org/data-science-metrics",
    packages=setuptools.find_packages(),
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


# %% CLEAN UP
# remove the excess files if package is installed with pip from github
# TODO: make tidals its own repository under tidepool_org
# once tidals becomes its own github repository, then this step will no longer be necessary
# TODO: publish tidals as a PyPi pacakge

files = glob.glob(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "*")))

hidFiles = glob.glob(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".*"))
)

allFiles = files + hidFiles

# if loaded from github with pip in environmental.yml, then when it will
# create a source file (src) and clone the entire data-analytics repo
for i in allFiles:
    # make sure you are in the src/tidals/ directory
    if "src" in i.split(sep=os.sep)[-3]:
        # delete all BUT files in tidals package
        if "tidepool-analysis-tools" not in i:
            if os.path.isdir(i):
                shutil.rmtree(i)
            else:
                os.remove(i)
