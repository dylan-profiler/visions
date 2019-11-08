Summarize
=========
We can also get a summary unique to the visions_type of the data

.. code-block:: python

    summarize(test_series, visions_datetime + missing)
    -> {
         'nunique': 3,
         'min': Timestamp('2010-01-01 00:00:00'),
         'max': Timestamp('2011-02-01 00:00:00'),
         'n_records': 4,
         'perc_unique': 1.0,
         'range': Timedelta('396 days 00:00:00'),
         'na_count': 1,
         'perc_na': 0.25
       }

If we had instead applied a summarization operation to a categorical series we would get

.. code-block:: python

    test_series = pd.Series(pd.Categorical([True, False, np.nan, 'test'], categories=[True, False, 'test', 'missing']))
    summarize(test_series, visions_categorical)
    -> {
        'nunique': 3,
        'n_records': 4,
        'category_size': 4,
        'missing_categorical_values': True,
        'na_count': 1,
        'perc_na': 0.25,
       }


.. seealso:: :doc:`Summaries example <examples/summaries>`

.. note:: Because `visions` types are nullable by default, they all inherit the same missing value summaries (`na_count`, and `perc_na`).
   New visions types :doc:`can be created <../creator/extending>` at will if you prefer to produce your own summaries or extend your analysis to other types of objects.
