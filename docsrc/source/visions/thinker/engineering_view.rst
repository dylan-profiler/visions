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

Missing value bitmaps
---------------------

TODO

Ref: `pandas 2.0 design document <https://dev.pandas.io/pandas2/internal-architecture.html#a-proposed-solution>`_
