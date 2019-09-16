Membership example
==================

The following example demonstrates the membership of several `tenzing_bool` series.


.. code-block:: python
    :caption: membership_example.py
    :name: membership_example

    import pandas as pd
    import numpy as np

    from tenzing.core.containers import MultiContainer, infinite, generic, missing, type
    from tenzing.core.model.types.tenzing_bool import tenzing_bool

    s1 = pd.Series([True, False], name="bool_series")
    s2 = pd.Series([True, False, np.nan], name="bool_nan_series")
    s3 = pd.Series([np.nan], name="nan_series")

    for s in [s1, s2, s3]:
        print(f'**{s.name}**')
        print(s in tenzing_bool, 'tenzing_bool')
        print(s in type[tenzing_bool], 'type[tenzing_bool]')
        print(s in missing, 'missing')
        print(s in MultiContainer([missing, type[tenzing_bool]]), '(missing, type[tenzing_bool])')
        print('')


Which prints:


.. code-block::

    **bool_series**
    True tenzing_bool
    True type[tenzing_bool]
    False missing
    False (missing)[type[tenzing_bool])

    **bool_nan_series**
    False tenzing_bool
    True type[tenzing_bool]
    True missing
    True (missing)[type[tenzing_bool])

    **nan_series**
    False tenzing_bool
    False type[tenzing_bool]
    True missing
    False (missing)[type[tenzing_bool])