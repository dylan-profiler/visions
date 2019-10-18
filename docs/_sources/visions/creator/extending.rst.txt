
Extending
=========

Custom Types
------------

Each Visions type is a singleton object extending the basic `VisionsBaseType` requiring a unique implementation of two methods:

1. `contains_op`. Checks whether a series is of the type visions_type, returns Bool.
2. `cast_op`. This is going away, needs to be folded into model_relations [TODO]


All visions_types can be made into `Option[visions_type]` by inheriting from `optionMixin` in `visions.core.Mixins`.

.. code-block:: python
    :caption: custom_type.py
    :name: custom_type

    from visions.core.models import VisionsBaseType

    class visions_timestamp(VisionsBaseType):
        def contains_op(self, series):
            return pdt.is_datetime64_dtype(series)

        def cast_op(self, series):
            return pd.to_datetime(series)


Custom Typesets
---------------

It is possible to use custom typesets.
The example below creates a custom typeset that only supports time-related types.

.. code-block:: python
    :caption: Custom time typeset

    class visions_custom_set(VisionTypeset):
        def __init__(self):
            types = [
                visions_datetime,
                visions_timedelta,
                visions_date,
                visions_time,
                visions_empty,
            ]
            containers = [missing, generic, type]
            super().__init__(containers, types)
