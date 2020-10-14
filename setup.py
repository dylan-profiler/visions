from pathlib import Path

from setuptools import find_packages, setup

# Read the contents of README file
source_root = Path(".")
with (source_root / "README.rst").open(encoding="utf-8") as f:
    long_description = f.read()

# Read the requirements
with (source_root / "requirements.txt").open(encoding="utf8") as f:
    requirements = f.readlines()

with (source_root / "requirements_dev.txt").open(encoding="utf8") as f:
    dev_requirements = f.readlines()

with (source_root / "requirements_test.txt").open(encoding="utf8") as f:
    test_requirements = f.readlines()

type_geometry_requires = ["shapely"]
type_image_path_requires = ["imagehash", "Pillow"]

extras_requires = {
    "type_geometry": type_geometry_requires,
    "type_image_path": type_image_path_requires,
    "plotting": ["pydot", "pygraphviz", "matplotlib"],
    "dev": dev_requirements,
    "test": test_requirements,
}

extras_requires["all"] = requirements + [
    dependency
    for name, dependencies in extras_requires.items()
    if name.startswith("type_") or name == "plotting"
    for dependency in dependencies
]


setup(
    name="visions",
    version="0.6.1",
    url="https://github.com/dylan-profiler/visions",
    description="Visions",
    author="Dylan Profiler",
    author_email="visions@ictopzee.nl",
    package_data={"vision": ["py.typed"]},
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=requirements,
    include_package_data=True,
    extras_require=extras_requires,
    tests_require=test_requirements,
    python_requires=">=3.6",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
