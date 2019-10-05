from setuptools import setup
from os.path import basename, splitext
from glob import glob
from setuptools import find_packages

type_geometry_requires = ["shapely", "geopandas==0.6.0"]
type_image_path_requires = ["imagehash", "PIL"]

install_requires = ["numpy", "pandas==0.25.1", "networkx", "tangled_up_in_unicode==0.0.3"] + \
                   type_geometry_requires + type_image_path_requires

extras_requires = {
    "type_geometry": type_geometry_requires,
    "type_image_path": type_image_path_requires,
    "network_plot": ["pydot", "pygraphviz"],
    "dev_docs": ["recommonmark", "sphinx_rtd_theme", "sphinx-autodoc-typehints"],
}

test_requires = [
    "pytest==5.2.0",
    "pytest-ordering",
    "pytest-rerunfailures",
    "pytest-sugar",
    "pytest-tldr",
    "pytest-runner"
]

setup(
    name="tenzing",
    version="0.0.4",
    description="Tenzing",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    install_requires=install_requires,
    include_package_data=True,
    extras_require=extras_requires,
    tests_require=test_requires,
    python_requires=">=3.5",
)
