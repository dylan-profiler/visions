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

.. seealso:: :doc:`Membership example <examples/membership>`

Cast
====

.. code-block:: python

    # Functional
    >>> from visions.core.functional import cast_type
    >>> cast_type(test_series)
    test_series

    # Object Oriented
    >>> from visions.core.implementations.typesets import visions_complete_set
    >>> typeset = visions_complete_set()
    >>> typeset.cast_series(test_series)
    test_series

.. seealso:: :doc:`Casting example <examples/casting>`
