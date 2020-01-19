Data Compression
================

Minimizing the memory used for a single type.
We can define a (lossless) conversion operation for specific types.
For example, we could convert a 64-bit integer to a 8-bit integer if it contains only pixel values.

decoupling semantic from physical allows to minimize the physical storage as long as the semantic type is preserved.
casting int64 to int32, text/categoricals may be encoded as string or dict, depending it cardinality,
dates can be encoded as numbers,
ip as numbers [4,5, 10].