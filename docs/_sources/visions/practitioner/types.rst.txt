Types
*****

Types are the fundamental unit within visions.
At their most fundamental, types must know how to test whether a sequence represents an instance of itself.
Beyond that types also understand their relationship with other types.

Membership
==========

Type membership is an important component of every visions type, membership checks answer the question `is my sequence of a type?`
In practice this looks like

.. code-block:: python

    >>> test_series in visions_string
    True

    >>> test_series in visions_integer
    False

.. seealso:: :doc:`Membership example <examples/membership>`
