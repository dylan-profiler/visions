from pathlib import Path

from setuptools import setup

from setuptools import find_packages


type_geometry_requires = ["shapely"]
type_image_path_requires = ["imagehash", "Pillow"]

install_requires = [
    "numpy",
    "pandas>=0.25.3",
    "networkx",
    "tangled_up_in_unicode>=0.0.3",
    "attrs",
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
    dependency
    for dependencies in extras_requires.values()
    for dependency in dependencies
]

test_requires = [
    "mypy",
    "pytest>=5.2.0",
    "pytest-ordering",
    "pytest-rerunfailures",
    "pytest-sugar",
    "pytest-tldr",
    "pytest-runner",
    "pytest-mypy",
    "pytest-black",
]

# Read the contents of README file
source_root = Path(".")
with (source_root / "README.rst").open(encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="visions",
    version="0.2.1",
    url="https://github.com/dylan-profiler/visions",
    description="Visions",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=install_requires,
    include_package_data=True,
    extras_require=extras_requires,
    tests_require=test_requires,
    python_requires=">=3.5",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
