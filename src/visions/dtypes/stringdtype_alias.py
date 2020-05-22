from typing import Type

from pandas import StringDtype
from pandas.core.arrays import StringArray
from pandas.core.dtypes.dtypes import registry


def create_alias(name: str) -> Type[StringDtype]:
    # Note that isinstance([Name]Dtype(), StringDtype()) == True

    # @classmethod
    # def _from_sequence(cls, scalars, dtype=None, copy=False):
    #     return super()._from_sequence(scalars, copy=copy)
    snake_name = "".join([part.capitalize() for part in name.split("_")])
    dtype = f"{snake_name}Dtype"
    arr = f"{snake_name}Array"

    alias_dtype = type(
        dtype, (StringDtype,), {"name": name, "__repr__": lambda self: dtype}
    )

    alias_array = type(arr, (StringArray,), {})

    def constructor(self, values, copy=False):
        super(alias_array, self).__init__(values, copy)
        self._dtype = alias_dtype()

    alias_array.__init__ = constructor
    alias_dtype.construct_array_type = classmethod(lambda cls: alias_array)

    registry.register(alias_dtype)

    return alias_dtype
