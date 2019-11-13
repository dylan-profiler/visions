
Extending
=========

Custom Types
------------

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

Custom Typesets
---------------

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

Another way of creating a typeset is by basing it on another typeset

.. code-block:: python
    :caption: Custom time typeset

    typeset = visions_complete_set() - visions_time + visions_date


.. seealso:: Engineer view on constraint checking