Data Summarization
==================

Data summarization and exploratory data analysis: couple specific analysis to specific types of data. [@pandasprofiling]

We can also get a summary unique to the visions_type of the data

.. code-block:: python

    >>> datetime_series = pd.Series([
    >>>    pd.datetime(2010, 1, 1),
    >>>    pd.datetime(2010, 8, 2),
    >>>    pd.datetime(2011, 2, 1),
    >>>    np.datetime64('NaT')
    >>> ])

    >>> summarizer = CompleteSummary()
    >>> summary = summarizer.summarize_series(datetime_series, visions_datetime)
    >>> summary
    {'dtype': dtype('<M8[ns]'),
     'frequencies': {Timestamp('2010-01-01 00:00:00'): 1,
                     Timestamp('2010-08-02 00:00:00'): 1,
                     Timestamp('2011-02-01 00:00:00'): 1},
     'max': Timestamp('2011-02-01 00:00:00'),
     'memory_size': 160,
     'min': Timestamp('2010-01-01 00:00:00'),
     'n_records': 4,
     'n_unique': 3,
     'na_count': 1,
     'range': Timedelta('396 days 00:00:00'),
     'types': {'NaTType': 1, 'Timestamp': 3}}

If we had instead applied a summarization operation to a categorical series we would get

.. code-block:: python

    >>> category_series = pd.Series(pd.Categorical([True, False, np.nan, 'test'], categories=[True, False, 'test', 'missing']))

    >>> summarizer = CompleteSummary()
    >>> summary = summarizer.summarize_series(category_series, visions_categorical)
    >>> summary
    {'category_size': 4,
     'dtype': CategoricalDtype(categories=[True, False, 'test', 'missing'], ordered=False),
     'frequencies': {False: 1, True: 1, 'missing': 0, 'test': 1},
     'memory_size': 495,
     'missing_categorical_values': True,
     'n_records': 4,
     'n_unique': 3,
     'na_count': 1,
     'ordered': False,
     'types': {'bool': 2, 'str': 1}}


Descriptive statistics
----------------------

In descriptive statistics we are looking for coefficients that summarize our data.
Describing numbers (for instance through the five-number summary) is completely different from describing strings.

The application is designed that each type in a typeset is associated with summary functions.
The summary of a sequence is the combination of all summary functions of the type and all its super types.
Examples from Integer, String, ExistingPath are given below.

Integer
~~~~~~~

.. figure:: ../../../../src/visions/visualisation/summaries/summary_integer.svg
   :width: 200 px
   :align: center
   :alt: Integer Summary Graph

   Integer Summary Graph

String
~~~~~~

.. figure:: ../../../../src/visions/visualisation/summaries/summary_string.svg
   :width: 200 px
   :align: center
   :alt: String Summary Graph

   String Summary Graph

Notably, the `text_summary` obtains awesome unicode statistics from another package within this project: `tangled up in unicode <https://github.com/dylan-profiler/tangled-up-in-unicode>`_.
If you are working with text data, you definitely want to check it out.

Existing Path
~~~~~~~~~~~~~

.. figure:: ../../../../src/visions/visualisation/summaries/summary_existing_path.svg
   :width: 300 px
   :align: center
   :alt: Existing Path Summary Graph

   Existing Path Summary Graph

Typeset summary graphs
----------------------

We can visualise the summary functions for the a typeset, too.

Complete Typeset
~~~~~~~~~~~~~~~~

.. figure:: ../../../../src/visions/visualisation/summaries/summary_complete.svg
   :width: 700 px
   :align: center
   :alt: CompleteTypeset Summary Graph

   CompleteTypeset Summary Graph


.. seealso:: :doc:`Summaries example <../getting_started/examples/summaries>`

.. note:: Because `visions` types are nullable by default, they all inherit the same missing value summaries (`na_count`).
   New visions types :doc:`can be created <../creator/extending>` at will if you prefer to produce your own summaries or extend your analysis to other types of objects.

`Pandas profiling <https://github.com/pandas-profiling/pandas-profiling>`_