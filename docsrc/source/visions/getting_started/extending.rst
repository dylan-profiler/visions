Extending
=========

Custom Type (from scratch)
---------------------------

Each ``visions`` type is a subclass of ``VisionsBaseType`` requiring a unique implementation of two methods:

1. ``get_relations``. Returns the set of relations mapping from another type to the current type.
2. ``contains_op``. Checks whether a series is of the type visions_type, returns Bool.

Let's inspect the source code for ``Ordinal`` to gather intuition.

.. code-block:: python
    :caption: visions.types.ordinal.py
    :name: Ordinal

    from visions.types.type import VisionsBaseType
    from visions.types.categorical import Categorical


    class Ordinal(VisionsBaseType):
        """**Ordinal** implementation of :class:`visions.types.VisionsBaseType`.
        Examples:
            >>> x = pd.Series([1, 2, 3, 1, 1], dtype='category')
            >>> x in visions.Ordinal
            True
        """

        @classmethod
        def get_relations(cls):
            return [IdentityRelation(cls, Categorical)]

        @classmethod
        def contains_op(cls, series: pd.Series, *args) -> bool:
            return pdt.is_categorical_dtype(series) and series.cat.ordered


In this example, ordinal declares a single ``IdentityRelation`` from categorical. The meaning
of ``IdentityRelation`` is not particularly important in this case, just know it means the mapping
function between categorical and ordinal is the identity function.

We can also see the ``contains_op`` requires the sequence to be an ordered categorical machine type representation.

Alternatively you can choose to base a type on an existing type.
This is convenient when you only change a single relation.

.. note::

    Your custom type might be helpful for others, in which case you can choose to contribute it to ``visions``.
    Read more on :doc:`how to contribute <../contributing/type>`.

Another example
---------------

The default typesets in ``visions`` consider ``Boolean`` and ``Categorical`` to be distinct types.
In fact, ``Boolean`` is a special case of ``Categorical`` where the number of categories is 2 and contains the values "True" and "False" ("Man" and "Woman" wouldn't be binary).

Note that for data analysis, the distinction makes sense.
For a boolean we could the true/false ratio for example.

See: ``examples/data_analysis`` for an example.

Custom Types (extend a type)
----------------------------

Another option is to create a new type based on an existing type.
This is useful for small changes, such as adding a single relation.

Each type has the method ``evolve_type`` for this purpose.

.. code-block:: python
   :caption: Add a inference relation from integer to datetime (YYYYMMDD)

    from visions.types.date_time import DateTime
    from visions.relations.integer_to_datetime import integer_to_datetime_year_month_day

    DateTimeIntYYYYMMDD = DateTime.evolve_type('int_yyyymmdd', lambda cls: [integer_to_datetime_year_month_day(cls)])

    print(DateTimeIntYYYYMMDD)
    # Prints: DateTime[int_yyyymmdd]

.. hint::

    While developing new type relations, you can use this helper function to debug:

    .. code-block:: python

       for column, type_before, type_after in compare_detect_inference_frame(df, typeset):
            print(f"{column} was {type_before} is {type_after}")


    Please read the ``Type changes`` section in the :doc:`functional API documentation <../api/functional>` for more details.


Custom Typesets (from scratch)
------------------------------

Although ``visions`` comes with an array of starter typesets suitable for most standard usage
you may quickly find yourself looking to expand upon those types to suit your own domain specific
needs. In order to meet those needs there are a number of easy mechanisms to either extend pre-existing
typesets or define your own from scratch.

For example, you could define a custom typeset with only time specific types as follows:

.. code-block:: python
    :caption: Custom time typeset

    class CustomSet(VisionTypeset):
        """Typeset that exclusively supports time related types

        Includes support for the following types:

        - DateTime
        - TimeDelta
        - Date
        - Time

        """

        def __init__(self):
            types = [
                DateTime,
                TimeDelta,
                Date,
                Time,
            ]
            super().__init__(types)


or even more simply,


.. code-block:: python
    :caption: Custom time typeset (simplified)

    import visions as v
    types = [v.DateTime, v.TimeDelta, v.Date, v.Time]
    CustomSet = VisionTypeset(types)


Custom typesets (extend typeset)
--------------------------------

Alternatively, typesets support a limited algebra allowing you to define new typesets
based on simple manipulations to pre-existing sets.

.. code-block:: python
    :caption: Custom time typeset

    import visions as v
    typeset = CompleteSet() - v.Time + v.Date

    # Alternatively
    typeset = typeset.replace(v.Time, v.Date)


Just like addition and subtraction elsewhere in Python, you can split these operations up
in any way imaginable:

.. code-block:: python

    import visions as v
    rdw_typeset = CompleteSet()
    rdw_typeset -= v.Boolean
    rdw_typeset += BooleanNL
    rdw_typeset -= v.Integer
    rdw_typeset += DateTimeIntYYYYMMDD
    rdw_typeset -= v.Categorical
    rdw_typeset += CategoricalStr
