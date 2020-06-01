#!/usr/bin/env python3

import setuptools

with open("Readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="orthophotomosaictiles",
    version="0.0.1",
    author="Adam Candy",
    author_email="adam@candylab.org",
    description="Project to create image tile sets for orthophotomosaics.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="None yet available",
    license="LGPLv3",
    packages=setuptools.find_packages(),
    scripts=['bin/orthophotomosaictiles'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
