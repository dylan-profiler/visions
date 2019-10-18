Typesets
********

Introduction
============

Types can also be organized into groups of types to perform analysis over a DataFrame or collection of series.
These are called visions typesets.

.. code-block:: python

    from visions.core.model_implementations.typesets import visions_standard

    my_typeset = visions_standard_set()
    my_typeset.types
    -> frozenset({visions_bool,
               visions_categorical,
               visions_complex,
               visions_float,
               visions_integer,
               visions_object,
               visions_string,
               visions_timestamp})


The standard typeset includes all of the baseline visions types.
A complete list of default typesets can be found in the API documentation.
Each typeset is unique to a dataset for caching purposes and can apply the same methods, like `summarize`, as a visions type.

.. code-block:: python

    df = pd.DataFrame({'a': range(3),
                         'b': [2 * i for i in range(3)],
                         'c': ['howdy', 'howdy', 'doody']})
    my_typeset.prep(df)



