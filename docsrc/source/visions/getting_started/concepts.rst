Concepts
========

This page introduces the concepts `visions` uses.

Data Type
---------

A data type is an abstraction of data that constrains the values that data can take.
`visions` considers types for sequences (in python: Tuples/Lists, pandas: Series, numpy: array, etc...).

.. seealso:: If you want a deeper understanding of data types, see :doc:`data type view <../thinker/data_type_view>`.

Typeset
-------

A typeset is literally a set of types and the relationships between them.
You can use typesets to specify different type systems.
The typeset contains types, comparable to a namespace for code or a virtual environment for dependencies.

Relational mapping
------------------

A relational mapping represents the relationships between types.
Visions creates a graph of these relationships within a typeset as a mechanism to perform type inference on data.
