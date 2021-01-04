Concepts
========

This page introduces the key concepts ``visions`` uses: types, typesets and type relations.

Types
-----

A data type is a logical abstraction constraining the set of values data can be composed from.
For example, *integers* can consist of values like 1, 2, and 3 but never 4.5.

Within the ``visions`` framework, types represent a logical abstraction over sequences of data
like python lists, numpy arrays, or pandas series.
These types might correspond to every day notions like integers, floats, strings, and datetimes or more complicated,
user configured ideas like geometries, fruits, or files. These logical, or semantic notions of type are
distinct from the machine representations of that data found on disk where, for example, the file
abstraction is represented on the computer as a string.

We use the terms *semantic type* and *machine type* to denote this difference.

.. seealso:: If you want a deeper understanding of data types, see :doc:`data type view <../background/data_type_view>`.

Typeset
-------

Typesets represent a mechanism to perform work over collections of types and contain
types in a way comparable to a namespace for code or a virtual environment for dependencies.
Flexible groupings of types allow different users to solve different problems in a manner specific to their circumstances.


Relational mapping
------------------

A relational mapping encodes the relationships between various types. These relationships come in
the form of two functions:

1. A relation function to test whether a mapping is possible between data of two types.
2. A mapping function defining the transformation between data of two types.

Each type is required to declare the set of potential relational mappings to itself upon
instantiation. Because types are purely self contained, it's possible to dynamically construct a
traversible graph of potential relations for any given typeset. This graph is then the mechanism used
to perform type inference on data.
