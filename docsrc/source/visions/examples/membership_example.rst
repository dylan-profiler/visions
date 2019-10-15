Membership example
==================

The following example demonstrates the membership of several `visions_bool` series.


.. literalinclude:: ../../../../notebooks/examples/membership_boolean.py
    :language: python
    :caption: membership_example.py
    :name: membership_example

Which prints:


.. code-block:: text

    **bool_series**
    True visions_bool
    True type[visions_bool]
    False missing
    False missing | type[visions_bool]

    **bool_nan_series**
    False visions_bool
    True type[visions_bool]
    True missing
    True missing | type[visions_bool]

    **nan_series**
    False visions_bool
    False type[visions_bool]
    True missing
    False missing | type[visions_bool]