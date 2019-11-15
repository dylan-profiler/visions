Concepts
========

This page introduces the concepts `visions` uses.

Types
-----

A data type is a logical abstraction constraining the types of values data can be composed from. For example,
`integers` can only consist of values like 1, 2, 3 but never 4.5.

Within the `visions` framework, Types represent a logical abstraction over sequences of data
(i.e. python: Tuples/Lists, pandas: Series, numpy: array, etc...). These types might correspond
to every day notions analysts might be familiar with like integers, floats, strings, datetimes, etc...
but also to be user configurable.

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
