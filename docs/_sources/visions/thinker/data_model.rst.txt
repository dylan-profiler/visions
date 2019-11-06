Unifying the Python, Numpy and Pandas data model
************************************************

The definitions that we need:

- Logical data types
- Physical data types
- Type detection
- Type inference
- Casting, coercion, conversion

Comparing to pandas
+++++++++++++++++++

There are multiple problems when working with pandas for data analysis:

- Missing values are handled inconsistently (int, bool, object)
- Strings are stored as objects

Decoupling physical and logical types
+++++++++++++++++++++++++++++++++++++
This package decouples physical and logical data types.
Physical data types describe the manner in which data is stored in memory.
Logical data types describe data on a more abstract level.
This separation is useful when we working with data that means something different to use, while being stored in the same physical data type.
A simple example is a set of URLs.
These are stored as strings, while not every string is an URL.
There are also operations that are only sensible on URLs and not on strings, such as extracting the url parts domain or protocol.

Problem with missing values
+++++++++++++++++++++++++++
Pandas' current data model is inconsistent with respect to missing values (i.e. `NaN` or `None`).
Adding missing values to integers and boolean results in upcasting the float and object respectively.
Implementing nullable integer and boolean logical types allow for more efficient storage.
This can be achieved through an internal bitmap (i.e. for each value keep track if it is missing yes or no).
https://dev.pandas.io/pandas2/internal-architecture.html#a-proposed-solution

Problem with strings
++++++++++++++++++++
Pandas does not have a logical type "string".
Strings are stored as objects, which gives non-trivial overhead
https://dev.pandas.io/pandas2/strings.html




The data models in Python, Numpy and Pandas are inconsistent and incomplete for logical storage of data types for analysis.
Here, we try to understand the aspects relation to what are shortcomings of the current implementation and we want of the unified data model.

We first provide a motivating example why we need a new model.
Secondly, we show what the data models of Python, Numpy and Pandas look like under the hood.
The third part of this page introduces the concepts needed to combine them.

We are envisioning a one-to-one correspondence between each of the data models without loss.
Types should be grouped together if they have the same analysis summary.



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

The Python data model (`docs <https://docs.python.org/3/reference/datamodel.html>`_)

.. image:: https://upload.wikimedia.org/wikipedia/commons/1/10/Python_3._The_standard_type_hierarchy.png
   :width: 424 px
   :align: center
   :alt: Python Data Model

Numpy
-----
- The Numpy data model (`docs <https://docs.scipy.org/doc/numpy-1.13.0/reference/arrays.scalars.html>`_)

.. image:: https://docs.scipy.org/doc/numpy/_images/dtype-hierarchy.png
   :width: 426 px
   :align: center
   :alt: Numpy Data Model

Pandas
------
- The Pandas data model (`docs <https://pandas.pydata.org/pandas-docs/stable/getting_started/basics.html#dtypes>`_)


+---------------+----------------------------------+
| Pandas Dtype  | Usage                            |
+===============+==================================+
| object        | Text or mixed                    |
+---------------+----------------------------------+
| int           | Integer                          |
+---------------+----------------------------------+
| float         | Floating point number            |
+---------------+----------------------------------+
| complex       | Complex numbers                  |
+---------------+----------------------------------+
| bool          | Boolean value                    |
+---------------+----------------------------------+
| datetime[ns]  | Date and time value              |
+---------------+----------------------------------+
| timedelta[ns] | Difference between two datetimes |
+---------------+----------------------------------+
| category      | Categorical values               |
+---------------+----------------------------------+
| Int           | Nullable integers                |
+---------------+----------------------------------+


Visions (Complete)
------------------
.. figure:: ../../../../examples/plots/typesets/typeset_complete.svg
   :width: 700 px
   :align: center
   :alt: CompleteTypeset Graph

   CompleteTypeset Graph


Unifying, what do we need?
==========================

Custom dtypes.


References
==========

We note that many of the problems `visions` attempts to solve, are discussed in the [design documents for pandas 2.0](https://dev.pandas.io/pandas2/) (2015-2016).