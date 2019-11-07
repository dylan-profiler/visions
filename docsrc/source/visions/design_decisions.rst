Design decisions
================

TODO: integrate in thinker
TODO: add axioma's (performant, extendible with sensible defaults, ...)

Nullable types
--------------
All types are nullable by default.

Memory usage
------------
Operations are designed to be idempotent (i.e. do not have side-effects).
This may impact the performance of your program when you use large DataFrames, as a copy is made.

