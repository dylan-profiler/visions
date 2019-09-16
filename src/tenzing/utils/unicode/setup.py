from setuptools import setup
from os.path import basename, splitext
from glob import glob
from setuptools import find_packages

setup(
    name="tangled_up_in_unicode",
    version="0.0.1",
    description="Tangled up in Unicode",
    install_requires=["pandas>=0.23.0"],
    include_package_data=True,
    python_requires=">=3.5",
)
