Data Summarization
==================

The process of exploratory data analysis (EDA) or data summarization intends to get a high-level overview of the main characteristics of a dataset.
This is an essential step when working with a new dataset, and therefore is worthwhile automating.

An effective summary of the dataset goes beyond the *physical* types of the dataset.
If a variable stores a URL as a string, we might be interested if every URL has the "https" scheme.
There is also overlap between physical types, where `min`, `max` and `range` are sensible statistics for real values as well as dates.


.. warning::
    Currently, the visions package contains the code for type summarization for demonstration purposes.
    Note that the core functionality for visions is type inference.
    The summarization functionality might be spun off in the future.
    Please use `pandas-profiling <https://github.com/pandas-profiling/pandas-profiling>`_, a dedicated package that provides these summarizations.

How does it work?
-----------------

Summaries are designed as *summary functions* on top of a `visions` typeset.
Each type in the set can be associated with a set of these functions.
The summary of a variable is the union of the output of the summary functions associated with its type or any of its supertypes.

Examples from Integer, Datetime and String types are given below.

Integer summary
~~~~~~~~~~~~~~~

.. figure:: ../../../../src/visions/visualisation/summaries/summary_integer.svg
   :width: 200 px
   :align: center
   :alt: Integer Summary Graph

   Integer Summary Graph

.. literalinclude:: ../../../../examples/summaries/integer_example.py
   :language: python
   :lines: 7-
   :lineno-start: 7
   :linenos:
   :caption: Integer Example (`view source <https://github.com/dylan-profiler/visions/tree/master/examples/summaries/integer_example.py>`__)


Datetime summary
~~~~~~~~~~~~~~~~


.. figure:: ../../../../src/visions/visualisation/summaries/summary_datetime.svg
   :width: 200 px
   :align: center
   :alt: DateTime Summary Graph

   DateTime Summary Graph

.. literalinclude:: ../../../../examples/summaries/datetime_example.py
   :language: python
   :lines: 6-
   :lineno-start: 6
   :linenos:
   :caption: DateTime Example (`view source <https://github.com/dylan-profiler/visions/tree/master/examples/summaries/datetime_example.py>`__)

String summary
~~~~~~~~~~~~~~

.. figure:: ../../../../src/visions/visualisation/summaries/summary_string.svg
   :width: 200 px
   :align: center
   :alt: String Summary Graph

   String Summary Graph


.. literalinclude:: ../../../../examples/summaries/string_example.py
   :language: python
   :lines: 6-
   :lineno-start: 6
   :linenos:
   :caption: String Example (`view source <https://github.com/dylan-profiler/visions/tree/master/examples/summaries/string_example.py>`__)

Notably, the `text_summary` obtains awesome Unicode statistics from another package within this project: `tangled up in unicode <https://github.com/dylan-profiler/tangled-up-in-unicode>`_.
If you are working with text data, you definitely want to check it out.


Typeset summary graphs
----------------------

We can visualise the summary functions of a typeset as a tree.

Complete Typeset
~~~~~~~~~~~~~~~~

.. figure:: ../../../../src/visions/visualisation/summaries/summary_complete.svg
   :width: 700 px
   :align: center
   :alt: CompleteTypeset Summary Graph

   CompleteTypeset Summary Graph


.. seealso:: :doc:`Summaries example <../getting_started/examples/summaries>`

.. note:: Because `visions` types are nullable by default, they all inherit the same missing value summaries (`na_count`).
   New visions types :doc:`can be created <../getting_started/extending>` at will if you prefer to produce your own summaries or extend your analysis to other types of objects.
