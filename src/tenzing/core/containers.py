from abc import abstractmethod
import numpy as np


class ContainerMeta(type):
    def __repr__(cls) -> str:
        return f"{cls.__name__}"


class Container(metaclass=ContainerMeta):
    @abstractmethod
    def mask(self, series):
        pass

    @abstractmethod
    def contains_op(self, series) -> bool:
        pass

    def __contains__(self, series) -> bool:
        try:
            return self.contains_op(series)
        except Exception:
            return False

    def __add__(self, other):
        if not isinstance(other, Container):
            raise Exception(f"{other} must be of type Container")
        return MultiContainer([self, other])


class MultiContainer(Container):
    def __init__(self, containers):
        assert len(containers) >= 2
        self.containers = containers

    def mask(self, series):
        mask = self.containers[0].mask(series)
        for container in self.containers[1:]:
            mask &= container.mask(series)
        return mask

    def contains_op(self, series, mask=[]) -> bool:
        return all(series in container for container in self.containers)

    def __repr__(self):
        return f"({', '.join([str(container.__class__) for container in self.containers])})"


class Generic(Container):
    def mask(self, series):
        return np.ones((len(series),), dtype=np.bool)

    def contains_op(self, series):
        return True


class Infinite(Container):
    def mask(self, series):
        return (~np.isfinite(series)) & series.notnull()

    def contains_op(self, series, mask=[]):
        return self.mask(series).any()


class Missing(Container):
    def mask(self, series):
        return series.notna()

    def contains_op(self, series, mask=[]):
        return series.hasnans


generic = Generic()
infinite = Infinite()
missing = Missing()


