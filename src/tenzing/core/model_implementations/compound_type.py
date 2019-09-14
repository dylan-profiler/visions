import numpy as np
import pandas as pd

# from tenzing.core.model_implementations.sub_type import subType

# TODO: Need to reconsider the naming, types should be distinguished from
# subtype / supertype / w/e they are finally called


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

    def get_mask(self, series):
        mask = np.zeros_like(series, dtype=bool)
        for type in self.types:
            mask |= type.get_mask(series)
        return mask

    def contains_op(self, series):
        if any(series not in type for type in self.types):
            return False

        mask = self.get_mask(series)
        return series[~mask] in self.base_type

    def base_summary(self, series):
        summary = {
            "frequencies": series.value_counts().to_dict(),
            "n_records": series.shape[0],
            "memory_size": series.memory_usage(index=True, deep=True),
            "dtype": series.dtype,
            "types": series.map(type).value_counts().to_dict(),
        }
        return summary

    def summarize(self, series):
        summary = self.base_summary(series)
        mask = self.get_mask(series)
        summary.update(self.base_type.summarize(series[~mask]))
        for type in self.types:
            summary.update(type.summarization_op(series))
        return summary

    def __contains__(self, item: pd.Series):
        if not isinstance(item, pd.Series):
            raise ValueError('Pandas series required')
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
        return f"Compound({', '.join([str(i) for i in self.types])})[{self.base_type}]"
