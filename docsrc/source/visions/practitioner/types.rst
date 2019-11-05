Types
*****

Let's take the example of a timestamp:

.. code-block:: python

    test_series = pd.Series([
        pd.datetime(2010, 1, 1),
        pd.datetime(2010, 8, 2),
        pd.datetime(2011, 2, 1),
        np.nan
    ])


Detection
=========

.. code-block:: python

    # Functional
    >>> from visions.core.functional import get_type
    >>> get_type(test_series)
    visions_datetime

    # Object Oriented
    >>> from visions.core.implementations.typesets import visions_complete_set
    >>> typeset = visions_complete_set()
    >>> typeset.get_series_type(test_series)
    visions_datetime


Inference
=========
Inference returns the narrowest possible type

Membership
==========
We can do a couple of things with this, first we can check if `test_series` is a `visions_timestamp`

.. code-block:: python

    >>> test_series in visions_datetime
    True

    >>> test_series in visions_boolean
    False


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

Because Visions types are `Option[type]` by default, they all inherit the same missing value summaries (`na_count`, and `perc_na`), however, new visions types can be created at will if you prefer to produce your own summaries or extend your analysis to other types of objects.

By default Visions includes implementations for the following types:

+-------------------------+---------+----------+----------+
| Type                    | Default | Geometry | Complete |
+=========================+=========+==========+==========+
| visions_integer         | Yes     | Yes      | Yes      |
+-------------------------+---------+----------+----------+
| visions_float           | Yes     | Yes      | Yes      |
+-------------------------+---------+----------+----------+
| visions_bool            | Yes     | Yes      | Yes      |
+-------------------------+---------+----------+----------+
| visions_categorical     | Yes     | Yes      | Yes      |
+-------------------------+---------+----------+----------+
| visions_complex         | Yes     | Yes      | Yes      |
+-------------------------+---------+----------+----------+
| visions_timestamp       | Yes     | Yes      | Yes      |
+-------------------------+---------+----------+----------+
| visions_object          | Yes     | Yes      | Yes      |
+-------------------------+---------+----------+----------+
| visions_string          | Yes     | Yes      | Yes      |
+-------------------------+---------+----------+----------+
| visions_geometry        | No      | Yes      | Yes      |
+-------------------------+---------+----------+----------+
| visions_path            | No      | No       | Yes      |
+-------------------------+---------+----------+----------+
| visions_existing_path   | No      | No       | Yes      |
+-------------------------+---------+----------+----------+
| visions_image_path      | No      | No       | Yes      |
+-------------------------+---------+----------+----------+
| visions_url             | No      | No       | Yes      |
+-------------------------+---------+----------+----------+
| visions_ip              | No      | No       | Yes      |
+-------------------------+---------+----------+----------+