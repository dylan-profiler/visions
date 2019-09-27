from abc import abstractmethod
import numpy as np
import pandas as pd


class PartitionerMeta(type):
    def __repr__(cls) -> str:
        return f"{cls.__name__}"


class Partitioner(metaclass=PartitionerMeta):
    @abstractmethod
    def mask(self, series):
        pass

    @abstractmethod
    def contains_op(self, series) -> bool:
        pass

    def partition(self, series) -> pd.Series:
        return series[self.mask(series)]

    def __contains__(self, series) -> bool:
        try:
            return self.contains_op(series)
        except Exception:
            return False

    def __add__(self, other):
        if not isinstance(other, Partitioner):
            raise Exception(f"{other} must be of type partitioner")
        return MultiPartitioner([self, other])

    def __repr__(self) -> str:
        return f"{self.__class__}"


class MultiPartitioner(Partitioner):
    def __init__(self, partitioners):
        assert len(partitioners) >= 2
        self.partitioners = partitioners

    def mask(self, series):
        mask = self.partitioners[0].mask(series)
        for partitioner in self.partitioners[1:]:
            mask &= partitioner.mask(series)
        return mask

    def contains_op(self, series, mask=None) -> bool:
        if mask is None:
            mask = []
        return all(series in partitioner for partitioner in self.partitioners)

    def __repr__(self):
        return f"({', '.join([str(partitioner.__class__) for partitioner in self.partitioners])})"


class Generic(Partitioner):
    def mask(self, series):
        return np.ones((len(series),), dtype=np.bool)

    def contains_op(self, series):
        return True

    @staticmethod
    def partition(series):
        return series


class Infinite(Partitioner):
    def mask(self, series):
        return (~np.isfinite(series)) & series.notnull()

    def contains_op(self, series, mask=None):
        if mask is None:
            mask = []
        return self.mask(series).any()


class Missing(Partitioner):
    def mask(self, series):
        return series.notna()

    def contains_op(self, series, mask=None):
        if mask is None:
            mask = []
        return series.hasnans


generic = Generic()
infinite = Infinite()
missing = Missing()


def get_series_partitioner(series, partitioners):
    series_partitioners = [
        partitioner for partitioner in partitioners if series in partitioner
    ]
    partitioner = (
        MultiPartitioner(series_partitioners)
        if len(series_partitioners) > 1
        else series_partitioners[0]
    )
    return partitioner