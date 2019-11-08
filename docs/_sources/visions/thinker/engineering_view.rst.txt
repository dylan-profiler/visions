Engineering view
================

This section discusses implementation of `visions`.
We find this view intuitive to create understanding of:

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

Dtypes
------
Staying close to pandas' data types, we can use the dtypes for type detection.
Complexity O(1) instead of O(n).

Constraint checking in tests
----------------------------
Constraint of mutual exclusivity is not checked on runtime, rather during testing.


Why don't we use OOP inheritance?
---------------------------------
You might wonder why for example `ImagePath` class does not inherit from `ExistingPath` class.
The short answer is, we tried, it didn't work out for the conditions we are under.
It is just not the abstraction that simplifies our problem, in fact it introduces complexity.
The current abstraction however, each type inherits from a base type, class inheritance from relations.

When you think how class inheritance would be beneficial is here, is where it reduces complexity.
TODO

Missing value bitmaps
---------------------

TODO

Ref: `pandas 2.0 design document <https://dev.pandas.io/pandas2/internal-architecture.html#a-proposed-solution>`_
