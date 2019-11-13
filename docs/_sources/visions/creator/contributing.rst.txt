Community contributions
***********************

You are welcome to contribute to the `visions` package.
This section contains information on the workflow when you want to add a contribution.

    When you build a tool, you do not know how it is going to be used.
    You try to improve the tool by looking how it is being used, and how people cut their fingers and stop that from happening.

    -- Bjarne Stroustrup


Installing dependencies
-----------------------

To get access to the development tools, you should have all dependencies installed.

.. code-block:: console

   pip install visions[dev_docs]

Testing
-------

Test `visions` with ``pytest``:


.. code-block:: console

   make test

Which is equivalent to

.. code-block:: console

   pytest --mypy --black tests/


Linting
-------

`visions` uses the `black` code style.

.. code-block:: console

   make lint

Which is equivalent to:

.. code-block:: console

   black .

Docs
----

The documentation needs to be generated after each contribution, because the API reference is automatically generated.
You can do this by:

.. code-block:: console

   make docs

This builds the docs using sphinx.

You can view the docs locally by going to the `docs/` folder and starting a web server, e.g.:

.. code-block:: console

   cd docs/
   python -m http.server


All together
------------

A shorthand for all commands above is:

.. code-block:: console

   make all