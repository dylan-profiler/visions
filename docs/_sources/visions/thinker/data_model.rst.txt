Unifying the Python, Numpy and Pandas data model
************************************************

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

- The pandas 2.0 Design Document (discussions 2015-2016): https://dev.pandas.io/pandas2/