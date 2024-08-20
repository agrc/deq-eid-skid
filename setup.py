#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
setup.py
A module that installs the DEQ EID skid as a module
"""
from pathlib import Path

from setuptools import find_packages, setup

project_folder = Path(__file__).parent / "src" / "deq_eid"

#: Load version from source file
version = {}
version_file = project_folder / "version.py"
exec(version_file.read_text(), version)

#: Load dependencies from requirements file so that we can keep a single source of truth
requirements_file = project_folder / "requirements.txt"
dependencies_txt = requirements_file.read_text()

setup(
    name="deq_eid",
    version=version["__version__"],
    license="MIT",
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    author="UGRC",
    author_email="ugrc-developers@utah.gov",
    url="https://github.com/agrc/deq-eid-skid",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=True,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
    ],
    project_urls={
        "Issue Tracker": "https://github.com/agrc/deq-eid-skid/issues",
    },
    keywords=["gis"],
    install_requires=dependencies_txt.strip().split("\n"),
    extras_require={
        "tests": [
            "pytest-cov>=3,<6",
            "pytest-instafail==0.5.*",
            "pytest-mock==3.*",
            "pytest-ruff==0.*",
            "pytest-watch==4.*",
            "pytest>=6,<9",
            "ruff==0.0.*",
        ]
    },
    setup_requires=[
        "pytest-runner",
    ],
    entry_points={
        "console_scripts": [
            "deq-eid-skid=deq_eid.main:process",
        ],
    },
)
