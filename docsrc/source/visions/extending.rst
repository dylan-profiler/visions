
Extending
=========

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
