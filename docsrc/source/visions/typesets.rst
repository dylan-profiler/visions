Typesets
********

Introduction
============

Types can also be organized into groups of types to perform analysis over a dataframe or collection of series.
These are called visions typesets.

.. code-block:: python

    from visions.core.model_implementations.typesets import tenzing_standard

    my_typeset = visions_standard_set()
    my_typeset.types
    -> frozenset({tenzing_bool,
               tenzing_categorical,
               tenzing_complex,
               tenzing_float,
               tenzing_integer,
               tenzing_object,
               tenzing_string,
               tenzing_timestamp})


The standard typeset includes all of the baseline visions types.
A complete list of default typesets can be found in the API documentation.
Each typeset is unique to a dataset for caching purposes and can apply the same methods, like `summarize`, as a visions type.

.. code-block:: python

    df = pd.DataFrame({'a': range(3),
                         'b': [2 * i for i in range(3)],
                         'c': ['howdy', 'howdy', 'doody']})
    my_typeset.prep(df)



Custom Typesets
===============

It is possible to use custom typesets.
The example below creates a custom typeset that only supports time-related types.

.. code-block:: python
    :caption: Custom time typeset

    class tenzing_custom_set(tenzingTypeset):
        def __init__(self):
            types = [
                tenzing_datetime,
                tenzing_timedelta,
                tenzing_date,
                tenzing_time,
                tenzing_empty,
            ]
            containers = [missing, generic, type]
            super().__init__(containers, types)
