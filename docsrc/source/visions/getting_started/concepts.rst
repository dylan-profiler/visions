Concepts
========

This page introduces the concepts `visions` uses.

Types
-----

A data type is a logical abstraction constraining the types of values data can be composed from. For example,
`integers` can only consist of values like `1`, `2`, `3` but never `4.5`.

Within the `visions` framework, Types represent a logical abstraction over sequences of data
(i.e. python: Tuples/Lists, pandas: Series, numpy: array, etc...). These types might correspond
to every day notions like integers, floats, strings, datetimes, etc... or more complicated,
user configured ideas like geometries, fruits, or files.

.. seealso:: If you want a deeper understanding of data types, see :doc:`data type view <../thinker/data_type_view>`.

Typeset
-------

Typesets represent a mechanism to perform work over groups of types. Typesets contain types
in a way comparable to a namespace for code or a virtual environment for dependencies.
Flexible groupings of types allow different users to solve different problems in a manner specific
to their circumstances.


Relational mapping
------------------

A relational mapping represents the relationships between types.
Visions creates a graph of these relationships within a typeset as a mechanism to perform type inference on data.
