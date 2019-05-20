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
        'pandas>=0.23.0',
        'numpy>=1.15',
        'shapely>=1.6',
        'jinja2>=2.7',
        'networkx>=2.2',
        'seaborn>=0.7.0',
        'matplotlib>=2.2.4'
    ],
    extras_require={'geopandas': ['geopandas'],
                    },
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-rerunfailures", "pytest-sugar", "pytest-tldr"],
    python_requires='>=3.4',
)
