Importing the module
********************

Before we proceed, we need to know where to find parts of visions and how to load them.
We find the easiest way to use the package to be:

.. code-block:: python

    import visions as v

From here we can access types, typesets and relations.

.. code-block:: python

    import visions as v

    # Types
    v.types.Integer
    v.types.DateTime

    # This also works
    v.Integer
    v.DateTime

    # Typesets
    v.typesets.CompleteSet

    # Also available through
    v.CompleteSet

    # Relations
    v.relations.relations.InferenceRelation

The types are used most often, you might prefer:

.. code-block:: python

    import visions.types as vt
    vt.Integer
    vt.DateTime

Alternatively, you could use the following syntax:

.. code-block:: python

    from visions.types import Integer, Path

This loads the types in the current namespace. One gotcha is that pathlib also has an object path: pathlib.Path will conflict with visions.Path.

.. warning::

	Don't import using `from visions.types import *`. This will load the modules that define types into the local namespace, overwriting reserved keywords as `complex` and `float`. `from visions import *` would work, but is discouraged. If you are unfamiliar with wildcard imports, please read this `stackoverflow answer <https://stackoverflow.com/a/2360808/470433>`_.

