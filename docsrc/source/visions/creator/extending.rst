
Extending
=========

Custom Types
------------

Each Visions type is a singleton object extending the basic `VisionsBaseType` requiring a unique implementation of two methods:

1. `get_relations`.
2. `contains_op`. Checks whether a series is of the type visions_type, returns Bool.


All visions_types can be made into `Option[visions_type]` by inheriting from `optionMixin` in `visions.core.Mixins`.

.. code-block:: python
    :caption: custom_type.py
    :name: custom_type

    from visions.core.models import VisionsBaseType

    class visions_timestamp(VisionsBaseType):
        @classmethod
        def get_relations(cls) -> dict:
            from visions.core.implementations.types import visions_generic

            relations = {
                visions_generic: relation_conf(inferential=False),
                visions_string: relation_conf(
                    relationship=test_utils.coercion_test(to_datetime),
                    transformer=to_datetime,
                    inferential=True,
                ),
            }
            return relations

        @classmethod
        def contains_op(cls, series):
            return pdt.is_datetime64_dtype(series)


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
