Typesets
********

Introduction
============

Types can also be organized into groups of types to perform analysis over a DataFrame or collection of series.
These are called visions typesets.

.. code-block:: python

    >>> from visions.core.implementations.typesets import visions_standard_set
    >>> my_typeset = visions_standard_set()
    >>> my_typeset.types
    {visions_datetime, visions_string, visions_generic, visions_timedelta, visions_integer, visions_complex, visions_bool, visions_object, visions_categorical, visions_float}



The standard typeset includes all of the baseline visions types.
A complete list of default typesets can be found in the API documentation.

.. code-block:: python

    df = pd.DataFrame({'a': range(3),
                       'b': [2 * i for i in range(3)],
                       'c': ['howdy', 'howdy', 'doody']})

Detection
=========

TODO

Inference
=========

TODO

Cast
====

TODO

.. seealso:: This returns a copy of your DataFrame object, please read the :doc:`engineering view <../thinker/engineering_view>` document for more information.
