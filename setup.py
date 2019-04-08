from setuptools import setup
from os.path import basename, splitext
from glob import glob
from setuptools import find_packages

setup(
    name="tenzing",
    version="0.0.1",
    description="Tenzing",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    install_requires=[
        'pandas',
        'numpy',
        'shapely',
        'jinja2',
        'PyYAML',
        'networkx'
    ],
    extras_require={
    },
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-rerunfailures", "pytest-sugar", "pytest-tldr"],
    python_requires='>=3.4',
)
