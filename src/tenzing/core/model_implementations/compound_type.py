import numpy as np

# from tenzing.core.model_implementations.sub_type import subType


class CompoundType(object):
    def __init__(self, base_type, types=None):
        if types is None:
            types = []

        from tenzing.core.models import tenzing_model
        from tenzing.core.model_implementations.sub_type import subType

        assert type(types) == list
        for typex in types:
            if not issubclass(typex, subType):
                raise ValueError("Only Sub types can be added to Compound types.")
        self.types = types

        if not issubclass(base_type, tenzing_model):
            raise ValueError("The base type should be tenzing model")
        self.base_type = base_type

    def contains_op(self, series):
        mask = np.zeros_like(series, dtype=bool)
        for type in self.types:
            mask |= type.get_mask(series)
        rest_mask = ~mask
        subs = all(series[type.get_mask(series)] in type for type in self.types)
        rest = series[rest_mask] in self.base_type
        return subs and rest

    def __contains__(self, item):
        return self.contains_op(item)

    def __add__(self, other):
        from tenzing.core.model_implementations.sub_type import subType

        if not issubclass(other, subType):
            raise ValueError("Only Sub types can be added to Compound types.")
        else:
            self.types.append(other)
        return self

    # def __str__(self):
    #     return f"CompoundType({self.types}, {self.base_type})"

    def __repr__(self):
        return f"{self.base_type}"
