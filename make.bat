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

IF "%1" == "pypi_package" (
	make install
    python setup.py sdist
    twine upload dist/*
    ECHO "PyPi package completed"
    GOTO end
)

IF "%1" == "lint" (
    black .
    GOTO end
)

IF "%1" == "install" (
	pip install -e .
	GOTO end
)

IF "%1%" == "all" (
    make lint
    make install
    make docs
    make test
    GOTO end
)

ECHO "No command matched"
:end
