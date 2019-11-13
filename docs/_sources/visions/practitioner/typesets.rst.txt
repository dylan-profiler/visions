Typesets
********

Introduction
============

Groups of types can be added together to perform analysis over data sequences like pandas series or dataframes.
These grouping are called typesets.

.. code-block:: python

    >>> from visions.core.implementations.typesets import visions_standard_set
    >>> typeset = visions_standard_set()
    >>> typeset.types
    {visions_datetime, visions_string, visions_generic, visions_timedelta, visions_integer, visions_complex, visions_bool, visions_object, visions_categorical, visions_float}


The standard typeset includes all of the baseline visions types.
A complete list of default typesets can be found in the API documentation.

Let's look at an example sequence of integers encoded as strings.

.. code-block:: python

    test_series = pd.Series(['1', '2', '3'])


Detection
=========

Type detection attempts to answer the question `What type is my data right now?`

.. code-block:: python

    # Functional
    >>> from visions.core.functional import type_detect_series
    >>> type_detect_series(test_series, typeset)
    visions_string

    # Object Oriented
    >>> from visions.core.implementations.typesets import visions_complete_set
    >>> typeset.detect_type_series(test_series)
    visions_string


Inference
=========

Type inference attempts to answer the question `What type is my data best represented as?``

.. code-block:: python

    >>> from visions.core.functional import type_detect_series, type_inference_series
    >>> type_detect_series(test_series, typeset)
    visions_string

    >>> type_inference_series(test_series, typeset)
    visions_integer

As you can see, visions was able to infer that our test_series was really a an integer series rather than a string series.
Integer detection is a fairly simple use case but using visions types of any degree of complexity from geometries to URLs to file paths and beyond.
Inference can be performed over any type included in a typeset.


Cast
====

Type casting is the process of converting a series or dataframe from one type to another, for example, from strings to integers.

.. code-block:: python

  >>> from visions.core.functional import type_cast_series
  >>> type_cast_series(test_series, typeset)
  pd.Series([1, 2, 3])

.. seealso:: This returns a copy of your data object, please read the :doc:`engineering view <../thinker/engineering_view>` document for more information.
