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
        'pandas==0.24.2',
        'numpy==1.16.2',
        'shapely==1.6.4.post2',
        'jinja2==2.10.1',
        'networkx==2.2'
    ],
    extras_require={
    },
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-rerunfailures", "pytest-sugar", "pytest-tldr"],
    python_requires='>=3.4',
)
