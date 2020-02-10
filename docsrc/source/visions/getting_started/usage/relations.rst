Type Relations
**************

All relations implement two methods `is_relation` and `transform`. `is_relation` is
responsible for testing the validity of a relation while `transform` applies whatever
transformation is required to map between the types defined on the relation.

Going back to our integer example.

.. code-block:: python

    >>> from visions import visions_integer
    >>> visions_integer.get_relations()
    [IdentityRelation(visions_generic -> visions_integer),
     InferenceRelation(visions_float -> visions_integer),
     InferenceRelation(visions_string -> visions_integer)]

Now imagine a series of floats like `[1.0, 2.0, 3.0]`.

.. code-block:: python

    >>> float_int_relation = visions_integer.get_relations()[1]
    >>> series = pd.Series([1.0, 2.0, 3.0])

    >>> series in visions_integer
    False

    >>> float_int_relation.is_relation(series)
    True

Not yet an integer, but it can be mapped to one!

.. code-block:: python

    >>> transformed_series = float_int_relation.transform(series)

    >>> transformed_series in visions_integer
    True

... and the `transform` method is how.

The relations between types represent the invisible bonds between types which allow
visions to map between them.
