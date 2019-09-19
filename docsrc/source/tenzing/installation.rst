Installation
============

You can install `package` from source and from pip

Pip
---

Installing with pip::

    pip install `package`


Source
-------------------

To install `package` from source, clone the repository from `github
<https://github.com/dylan-profiling/package>`_::

    git clone https://github.com/dylan-profiling/package.git
    cd package
    python setup.py install .


Testing
-------

Test `package` with ``pytest``::

    cd package
    pytest

Requirements
------------

* pandas
* numpy
* networkx
* TODO: optional requirements