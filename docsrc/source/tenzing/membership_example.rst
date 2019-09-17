Membership example
==================

The following example demonstrates the membership of several `tenzing_bool` series.


.. literalinclude:: ../../../notebooks/examples/membership_boolean.py
    :language: python
    :caption: membership_example.py
    :name: membership_example

Which prints:


.. code-block:: text

    **bool_series**
    True tenzing_bool
    True type[tenzing_bool]
    False missing
    False missing | type[tenzing_bool]

    **bool_nan_series**
    False tenzing_bool
    True type[tenzing_bool]
    True missing
    True missing | type[tenzing_bool]

    **nan_series**
    False tenzing_bool
    False type[tenzing_bool]
    True missing
    False missing | type[tenzing_bool]