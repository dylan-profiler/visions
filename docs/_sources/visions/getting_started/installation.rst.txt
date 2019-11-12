Installation
============

You can install `visions` from source and from pip

Pip
---

Installing with pip:

.. code-block:: console

    pip install visions[all]


By default, `visions` includes dependencies for additional types such as images and geodata.
You can install a more lightweight version by installing only the specific dependencies you really need:


.. code-block:: console

    # Minimal example
    pip install visions

    # Only geometry
    pip install visions[type_geometry]


Source
------

To install `visions` from source, clone the repository from `github
<https://github.com/dylan-profiling/visions>`_:

.. code-block:: console

    git clone https://github.com/dylan-profiling/visions.git
    cd package
    python setup.py install .



Requirements
------------

The requirements are listed in `setup.py`.
