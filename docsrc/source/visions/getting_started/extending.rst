Extending
=========

Custom Type (from scratch)
---------------------------

Each `visions` type is class extending the basic `VisionsBaseType` requiring a unique implementation of two methods:

1. `get_relations`. Returns relations directed towards other types.
2. `contains_op`. Checks whether a series is of the type visions_type, returns Bool.

To get some intuition, we can have a look at the source code of any type, in this case `visions_ordinal`.

.. code-block:: python
    :caption: visions_ordinal.py
    :name: visions_ordinal

    from visions.core.models import VisionsBaseType

    def _get_relations():
        from visions.core.implementations.types import visions_categorical

        relations = [IdentityRelation(visions_ordinal, visions_categorical)]
        return relations

    class visions_ordinal(VisionsBaseType):
        """**Ordinal** implementation of :class:`visions.core.model.type.VisionsBaseType`.
        Examples:
            >>> x = pd.Series([1, 2, 3, 1, 1], dtype='category')
            >>> x in visions_ordinal
            True
        """

        @classmethod
        def get_relations(cls):
            return _get_relations()

        @classmethod
        def contains_op(cls, series: pd.Series) -> bool:
            return pdt.is_categorical_dtype(series) and series.cat.ordered




Alternatively you can choose to base a type on an existing type.
This is convenient when you only change a single relation.

.. code-block:: python

    visions



.. note::

    Your custom type might be helpful for others, in which case you can choose to contribute it to `visions`.
    Read more on :doc:`how to contribute <../contributing/type>`.


Custom Type (extend type)
-------------------------

Another option is to create a new type based on an existing type.
This is useful for small changes, such as adding a single relation.

Each type has the method `extend_relations` for this purpose.

.. code-block:: python
   :caption: Add a inference relation from integer to datetime (YYYYMMDD)

    from visions.core.implementations.types.visions_integer import _get_relations, visions_integer
    from visions.lib.relations.integer_to_datetime import integer_to_datetime_year_month_day

    compose_relations = lambda: _get_relations() + [integer_to_datetime_year_month_day()]
    visions_integer_ddt = visions_integer.extend_relations('with_datetime', compose_relations)

    print(visions_integer_ddt)
    # Prints: visions_integer[with_datetime]

.. hint::

    While developing new type relations, you can use this helper function to debug:

    .. code-block:: python

       for column, type_before, type_after in compare_detect_inference_frame(df, typeset):
            print(f"{column} was {type_before} is {type_after}")


Custom Typesets (from scratch)
------------------------------

It is possible to use custom typesets.
The example below creates a custom typeset that only supports time-related types.

.. code-block:: python
    :caption: Custom time typeset

    class visions_custom_set(VisionTypeset):
        """Typeset that exclusively supports time related types

        Includes support for the following types:

        - visions_datetime
        - visions_timedelta
        - visions_date
        - visions_time

        """

        def __init__(self):
            types = [
                visions_datetime,
                visions_timedelta,
                visions_date,
                visions_time,
            ]
            super().__init__(types)


Custom typesets (extend typeset)
--------------------------------

Another way of creating a typeset is by basing it on another typeset

.. code-block:: python
    :caption: Custom time typeset

    typeset = visions_complete_set() - visions_time + visions_date

When performing multiple additions and/or subtractions, the above will become a long list.
Just like other addition and subtraction in Python, you can split the operations:

.. code-block:: python

    rdw_typeset = visions_complete_set()
    rdw_typeset -= visions_bool
    rdw_typeset += visions_bool_nl
    rdw_typeset -= visions_integer
    rdw_typeset += visions_integer_ddt
    rdw_typeset -= visions_categorical
    rdw_typeset += visions_categorical_str

.. seealso:: Engineer view on constraint checking