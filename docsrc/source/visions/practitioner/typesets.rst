Typesets
********

Introduction
============

Groups of types can be combined to perform analysis over data sequences like pandas series or dataframes.
These type grouping are called typesets.

.. code-block:: python

    >>> from visions.core.implementations.typesets import visions_standard_set
    >>> typeset = visions_standard_set()
    >>> typeset.types
    {visions_datetime, visions_string, visions_generic, visions_timedelta,
    visions_integer, visions_complex, visions_bool, visions_object, visions_categorical, visions_float}

The standard typeset includes all baseline visions types; a
complete list of default typesets is available in the API documentation.

Broadly speaking, a typeset exposes three primary capabilities - type detection, type inference,
and type casting.

Let's look at an example sequence of integers encoded as strings to see these capabilities in action.

.. code-block:: python

    test_series = pd.Series(['1', '2', '3'])


Detection
=========

Type detection attempts to answer the question: `What type is my data right now?`

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

Type inference attempts to answer the question: `What type is my data best represented as?``

.. code-block:: python

    >>> from visions.core.functional import type_detect_series, type_inference_series
    >>> type_detect_series(test_series, typeset)
    visions_string

    >>> type_inference_series(test_series, typeset)
    visions_integer

As you can see, visions was able to infer that the test_series was really an integer series rather than string.
Integer detection is a fairly simple use case but visions supports arbitrarily complex types from geometries to URLs to file paths and beyond.




Cast
====

Type casting is the process of converting a series or dataframe from one type to another, for example, from strings to integers.

.. code-block:: python

  >>> from visions.core.functional import type_cast_series
  >>> type_cast_series(test_series, typeset)
  pd.Series([1, 2, 3])

.. seealso:: This returns a copy of your data object, please read the :doc:`engineering view <../thinker/engineering_view>` document for more information.


Details
=======

The Generic Typeset
-------------------

All typesets include the `visions_generic` type at their base. The generic represents a catch all type
to which all sequences belong. This means an "empty" typeset would still include a generic at it's root
from which all other types can be related.

.. code-block:: Python

  >>> from visions.core.model.typeset import VisionsTypeset
  >>> my_typeset = VisionsTypeset([])
  >>> my_typeset.types
  {visions_generic}


Multiple Typesets
-----------------

Another potential "gotcha" is to remember that all operations are defined over the specific typeset
used to invoke the operation. In practice this means two different typesets might infer or detect
different types for the same series.

Let's take the example of two typesets: one including the integer type and one without.

.. code-block:: Python

  >>> from visions.core.model.typeset import VisionsTypeset
  >>>
  >>> typeset_1 = VisionsTypeset([visions_integer, visions_float])
  >>> typeset_2 = VisionsTypeset([visions_float])
  >>>
  >>> series = pd.Series([1, 2, 3])

Logically we can see the series should be an integer but what happens when attempting inference
with the two different typesets?

.. code-block:: Python

  >>> typeset_1.detect_type_series(series)
  visions_integer

Excellent, we got what we expected! What about the second typeset which omits the integer type?

.. code-block:: Python

  >>> typeset_2.detect_type_series(series)
  visions_generic

Because integers weren't included in the typeset we didn't detect them. Instead, the closest
matching type included in the typeset was returned.

The traversal graph for the default typeset can be viewed below. The relation graph constructed
for any specific typeset will vary based on the relations implemented on each type included in
the typeset.

.. figure:: ../../../../src/visions/visualisation/typesets/typeset_complete_base.svg
   :width: 700 px
   :align: center
   :alt: Visualisation of the base data structure of the *visions_complete_set*.

   Visualisation of the base data structure of the *visions_complete_set*.
