Data Compression
================

Decoupling *semantic* data types from *physical* data types makes it easier to compress variables.
For this example, we restrict ourselves to in-memory compression.
Our task is to automatically obtain an efficient in-memory representation, to minimize the RAM used while preserving the same semantic type.

A typical task is data compression, where the user seeks to minimize memory utilization of the *machine* type representation while preserving the *semantic* type of their data.
We consider a dataset with one variable consisting of "Yes" and "No" values.
As the variable has only two distinct values, the *machine* type storage needed can be optimally stored as a bool using only one byte per value as opposed to a pandas object using approximately 66 bytes.
There are infinite potential ways to denote "Yes" and "No" values within a dataset, consequently, we cannot rely on a static rule-based system for inference in general-purpose software.
However, that does not mean that this is "just data munging" and we cannot do this and other tasks more effectively.
We observe that some patterns occur more often ("Yes", "No" over "Arr" or "Nay") and there are other indicators that can help a system to decide what to do (the variable two distinct values).
We note that a rule-based system that trivially encodes each variable with two distinct values as boolean is no solution, as the encoding loses part of it's meaning (e.g. encoding "Male", "Female").

Compressio
----------

Compressio performs this lossless in-memory compression of pandas DataFrames and Series powered by the visions type system. 
This may yield up to 10x less RAM usage for the same data.

For the code, examples and an analysis of pandas' types, you can visit the `Project Homepage <https://github.com/dylan-profiler/compressio>`_.
