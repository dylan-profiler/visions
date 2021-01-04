Installation
============

You can install ``visions`` from source and from pip

Pip
---

Installing with pip:

.. code-block:: console

    pip install visions[all]


By default, ``visions`` installs the complete set of dependencies, including for specialized types such as images and geodata.
This is great for experimenting, however once you have settled on a set of types, it is recommended to slim down the dependencies.
It is possible to obtain a more lightweight installation by installing only the specific dependencies you really need:

* ``type_geometry`` for ``Geometry``
* ``type_image_path`` for ``Image``

.. code-block:: console

    # Minimal example: only install the default types
    pip install visions

    # Default and geometry dependencies
    pip install visions[type_geometry]

    # Multiple dependency sets
    pip install visions[type_geometry,type_image_path]

For additional dependencies (plotting, development, testing), please read the `contribution page <../creator/contributing>`_.

Source
------

To install ``visions`` from source, clone the repository from `github <https://github.com/dylan-profiling/visions>`_:

.. code-block:: console

    git clone https://github.com/dylan-profiling/visions.git
    cd package
    python setup.py install .

Requirements
------------

The requirements are listed in ``setup.py`` and the files ``requirements.txt``, ``requirements_dev.txt`` and ``requirements_test.txt``.
