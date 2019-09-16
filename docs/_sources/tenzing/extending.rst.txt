
Extending
=========

Each Tenzing type is a singleton object extending the basic `tenzing_model` requiring a unique implementation of two methods:

1. `contains_op`. Checks whether a series is of the type tenzing_type, returns Bool.
2. `cast_op`. This is going away, needs to be folded into model_relations [TODO]


All tenzing_types can be made into `Option[tenzing_type]` by inheriting from `optionMixin` in `tenzing.core.Mixins`.

.. code-block:: python
	:caption: custom_type.py
	:name: custom_type

	from tenzing.core.models import tenzing_model

	class tenzing_timestamp(tenzing_model):
		def contains_op(self, series):
			return pdt.is_datetime64_dtype(series)

		def cast_op(self, series):
			return pd.to_datetime(series)
