from setuptools import setup
from os.path import basename, splitext
from glob import glob
from setuptools import find_packages


type_geometry_requires = ["shapely"]
type_image_path_requires = ["imagehash", "Pillow"]

install_requires = [
    "numpy",
    "pandas>=0.25.3",
    "networkx",
    "tangled_up_in_unicode>=0.0.3",
    "attr",
]

extras_requires = {
    "type_geometry": type_geometry_requires,
    "type_image_path": type_image_path_requires,
    "network_plot": ["pydot", "pygraphviz", "matplotlib"],
    "dev": [
        "black",
        "mypy",
        "recommonmark",
        "sphinx_rtd_theme",
        "sphinx-autodoc-typehints",
    ],
}

extras_requires["all"] = install_requires + [
    dependency for dependency in extras_requires.values()
]

test_requires = [
    "mypy",
    "black",
    "pytest>=5.2.0",
    "pytest-ordering",
    "pytest-rerunfailures",
    "pytest-sugar",
    "pytest-tldr",
    "pytest-runner",
    "pytest-mypy",
    "pytest-black",
]

setup(
    name="visions",
    version="0.1.2",
    description="Visions",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    install_requires=install_requires,
    include_package_data=True,
    extras_require=extras_requires,
    tests_require=test_requires,
    python_requires=">=3.6",
)
