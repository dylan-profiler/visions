Types
*****

Let's take the example of a timestamp:

.. code-block:: python

    test_series = pd.Series([
        pd.datetime(2010, 1, 1),
        pd.datetime(2010, 8, 2),
        pd.datetime(2011, 2, 1),
        np.datetime64('NaT')
    ])


Detection
=========

.. code-block:: python

    # Functional
    >>> from visions.core.functional import type_detect_series
    >>> type_detect_series(test_series)
    visions_datetime

    # Object Oriented
    >>> from visions.core.implementations.typesets import visions_complete_set
    >>> typeset = visions_complete_set()
    >>> typeset.detect_type_series(test_series)
    visions_datetime


Inference
=========

Inference tries to cast certain series:

.. code-block:: python

    >>> from visions.core.functional import type_detect_series, type_inference_series
    >>> integer_series = pd.Series(["1", "2", "3", "4"])
    >>> type_detect_series(integer_series)
    visions_string
    >>> type_inference_series(integer_series)
    visions_integer


Membership
==========
We can do a couple of things with this, first we can check if `test_series` is a `visions_timestamp`

.. code-block:: python

    >>> test_series in visions_datetime
    True

    >>> test_series in visions_boolean
    False

.. seealso:: :doc:`Membership example <examples/membership>`

Cast
====

.. code-block:: python

    # Functional
    >>> from visions.core.functional import type_cast_series
    >>> type_cast_series(integer_series)
    0    1
    1    2
    2    3
    3    4
    dtype: int64

    # Object Oriented
    >>> from visions.core.implementations.typesets import visions_complete_set
    >>> typeset = visions_complete_set()
    >>> typeset.cast_series(integer_series)
    0    1
    1    2
    2    3
    3    4
    dtype: int64

.. seealso:: :doc:`Casting example <examples/casting>`
