Community contributions
***********************

Contributions are welcome to the ``visions`` package! Please insure all contributions
abide by the guidelines outlined below.

    *When you build a tool, you do not know how it is going to be used.*
    *You try to improve the tool by looking how it is being used, and how people cut their fingers and stop that from happening.*

    -- Bjarne Stroustrup


Installing dependencies
-----------------------

To get access to the development tools, you should have all dependencies installed.

.. code-block:: console

   pip install visions[dev,test,plotting]

Testing
-------

Test ``visions`` with ``pytest``:


.. code-block:: console

   make test

Which is equivalent to

.. code-block:: console

   pytest --mypy --black tests/


Linting
-------

``visions`` uses the ``black`` code style, ``isort`` for sorting imports and ``pyupgrade`` for updating python syntax.

.. code-block:: console

   make lint

Which is equivalent to:

.. code-block:: console

   pre-commit run --all-files


Documentation
-------------

Software should provide adequate documentation for beginning and advanced users.
When you contribute, please check if your contribution requires some additional documentation.
Documentation is written in ReStructuredText (.rst).
You can find the source files in ``docsrc\source\visions\``.

The documentation is automatically generated after each contribution by our `Github Actions <https://github.com/dylan-profiler/visions/actions>`_ workflow.

If you like, you can manually generate the documentation by running:

.. code-block:: console

   make docs

This builds the docs using sphinx.

You can view the docs locally by going to the ``docs/`` folder and starting a web server, e.g.:

.. code-block:: console

   cd docs/
   python -m http.server


All together
------------

A shorthand for all commands above is:

.. code-block:: console

   make all
