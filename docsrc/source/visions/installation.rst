Installation
============

You can install `visions` from source and from pip

Pip
---

Installing with pip::

    pip install visions


Source
-------------------

To install `visions` from source, clone the repository from `github
<https://github.com/dylan-profiling/visions>`_::

    git clone https://github.com/dylan-profiling/visions.git
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