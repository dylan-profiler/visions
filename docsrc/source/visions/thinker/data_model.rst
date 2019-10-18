Unifying the Python, Numpy and Pandas data model
************************************************

The data models in Python, Numpy and Pandas are inconsistent and incomplete for logical storage of data types for analysis.
Here, we try to understand the aspects relation to what are shortcomings of the current implementation and we want of the unified data model.

We first provide a motivating example why we need a new model.
Secondly, we show what the data models of Python, Numpy and Pandas look like under the hood.
The third part of this page introduces the concepts needed to combine them.

Where the current models fail
=============================

Motivating example: Nullable Boolean

Motivating example: Nullable Integer / Float

Motivating example: Objects

.. Visions creates an internal type system representing the type of a pandas series rather than the underlying types of it's constituent objects.
   This allows us to flexibly perform sets of well defined operations over things like `Option[integer]` which might otherwise be upcast by pandas into `float`.
   This also allows us to produce more interesting summaries for data which might otherwise simply be represented in pandas as `object`.

How do Python, Numpy and Pandas model data?
===========================================

Python
------

The Python data model (`docs <https://docs.python.org/3/reference/datamodel.html>`_) (`diagram <https://en.wikipedia.org/wiki/Data_type#/media/File:Python_3._The_standard_type_hierarchy.png>`_)

Numpy
-----
- The Numpy data model (`docs <https://docs.scipy.org/doc/numpy-1.13.0/reference/arrays.scalars.html>`_) (`diagram <https://docs.scipy.org/doc/numpy-1.13.0/_images/dtype-hierarchy.png>`_)

Pandas
------
- The Pandas data model (`docs <https://pandas.pydata.org/pandas-docs/stable/getting_started/basics.html#dtypes>`_) (`diagram <https://pbpython.com/images/pandas_dtypes.png>`_)


Unifying, what do we need?
==========================

Custom dtypes.



References
==========

- The pandas 2.0 Design Document (discussions 2015-2016): https://dev.pandas.io/pandas2/