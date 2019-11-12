Engineering view
================

This section discusses the core implementation of `visions`.
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
You might wonder why for example `ImagePath` class does not inherit from `ExistingPath` class.
The short answer is, we tried, in order to support our use cases inheritance ultimately only added complexity to the solution.
Within the current abstraction, each type inherits from a base type, class inheritance from relations.

When you think how class inheritance would be beneficial is here, is where it reduces complexity.
TODO

Sampling in inference
---------------------
TODO

Why are relations defined on the type?
--------------------------------------
The short answer is extendability.

Recall, relations define mappings to a type, so, given two types `A` and `B` with a relation from `B -> A`,
that relationship is defined on `A`. Defining relationships in this way actually decouples types from each other.
This allows us to dynamically construct a relation graph based only on the types included in the typeset without
modifying any type specific logic.


Missing value bitmaps
---------------------
TODO

Ref: `pandas 2.0 design document <https://dev.pandas.io/pandas2/internal-architecture.html#a-proposed-solution>`_
