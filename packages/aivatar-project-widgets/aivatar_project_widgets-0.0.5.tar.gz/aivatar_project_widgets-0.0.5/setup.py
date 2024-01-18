"""Describe our module distribution to Distutils."""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import third-party modules
from setuptools import find_packages
from setuptools import setup

setup(
    name="aivatar_project_widgets",
    author="lavenderyao",
    author_email="lavenderyao@tencent.com",
    url="https://git.woa.com/DCC_Client/Framework/aivatar_project_widgets",
    package_dir={"": "."},
    packages=find_packages("."),
    description="widgets for aivatar_project_widgets",
    entry_points={},
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    package_data={
        "": ["*.png"],
    },
    install_requires=['aivatar_project_api>=0.0.0, <0.1.0', "Qt.py"],
    # setup_requires=["setuptools_scm"],
)
