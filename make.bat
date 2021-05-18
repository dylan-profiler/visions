@echo off
setlocal enabledelayedexpansion

IF "%1%" == "docs" (
	cd docsrc/ && make github
    ECHO "Docs updated!"
    GOTO end
)

IF "%1" == "test" (
    pytest tests/
    ECHO "Tests completed!"
    GOTO end
)

IF "%1" == "plots" (
    cd src/visions/visualisation/
    python plot_circular_packing.py
    python plot_summary.py
    python plot_typesets.py
    ECHO "Plots completed!"
    GOTO end
)

IF "%1" == "pypi_package" (
    make install
    check-manifest
    python setup.py sdist bdist_wheel
    twine check dist/*
    twine upload --skip-existing dist/*
    ECHO "PyPi package completed"
    GOTO end
)

IF "%1" == "lint" (
    pre-commit run --all-files
    GOTO end
)

IF "%1" == "install" (
	pip install -e .
	GOTO end
)

IF "%1%" == "all" (
    make lint
    make install
    make plots
    make docs
    make test
    GOTO end
)

ECHO "No command matched"
:end
