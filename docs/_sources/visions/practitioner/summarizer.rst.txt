Summarize
=========
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


.. seealso:: :doc:`Summaries example <examples/summaries>`

.. note:: Because `visions` types are nullable by default, they all inherit the same missing value summaries (`na_count`).
   New visions types :doc:`can be created <../creator/extending>` at will if you prefer to produce your own summaries or extend your analysis to other types of objects.
