Design decisions
================

This section discusses the core implementation of ``visions``.
This view can guide intuition of:

- performance and complexity of operations

It is limited for:

- understanding abstract concepts
- motivation for representations

Short circuiting
----------------

TODO

Sampling
--------

TODO

Memory usage
------------
TODO

Operations are designed to be idempotent (i.e. do not have side-effects).
This may impact the performance of your program when you use large DataFrames, as a copy is made.

Dtypes
------
Staying close to pandas' data types, we can use the dtypes for type detection.
Complexity O(1) instead of O(n).

Constraint checking in tests
----------------------------
Constraint of mutual exclusivity is not checked on runtime, rather during testing.


Nullable types
--------------
All types are nullable by default.
TODO: why (refer to goal)

Why don't we use OOP inheritance?
---------------------------------
You might wonder why for example ``Image`` class does not inherit from ``File`` class.
The short answer is, we tried, in order to support our use cases inheritance ultimately only added complexity to the solution.
Within the current abstraction, each type inherits from a base type, class inheritance from relations.

When you think how class inheritance would be beneficial is here, is where it reduces complexity.
TODO
`The End Of Object Inheritance & The Beginning Of A New Modularity <https://www.youtube.com/watch?v=3MNVP9-hglc>`_

.. note::
    The choice of not using OOP inheritance limits the use of build-in type hints that rely on covariance and contravariance.
    Read more in `PEP 484 <https://www.python.org/dev/peps/pep-0483/#covariance-and-contravariance>`_.

Sampling in inference
---------------------
TODO

Why are relations defined on the type?
--------------------------------------
The short answer is extendability.

Recall, relations define mappings to a type, so, given two types ``A`` and ``B`` with a relation from ``B -> A``,
that relationship is defined on ``A``. Defining relationships in this way actually decouples types from each other.
This allows us to dynamically construct a relation graph based only on the types included in the typeset without
modifying any type specific logic.


Missing value bitmaps
---------------------
Pandas upcasts certain types when adding missing values, unnecessarily increasing physical storage size.
This behaviour `occurs for booleans and integers <https://pandas.pydata.org/pandas-docs/stable/user_guide/missing_data.html#missing-data-casting-rules-and-indexing>`_.
Pandas itself offers `nullable integers <https://pandas.pydata.org/pandas-docs/stable/user_guide/integer_na.html#integer-na>`_.
We implement nullable types as missing value bitmaps, in the same way pandas' nullable integers work.
For each value, we keep a 1 bit per value that specifies whether a value is null or not.
We use the contention that ``NaN`` is used when the type represents numbers, ``None`` otherwise.
More information can be found here: `pandas 2.0 design document <https://dev.pandas.io/pandas2/internal-architecture.html#a-proposed-solution>`_
