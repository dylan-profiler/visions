from abc import abstractmethod
import numpy as np
import pandas as pd

from tenzing.core.model.types import tenzing_generic


class ContainerMeta(type):
    def __str__(cls) -> str:
        return f"{cls.__name__}"

    def __repr__(cls) -> str:
        return str(cls)

    def __add__(self, other):
        """
        Examples:
            >>> Generic + Infinite
        """
        if not isinstance(other, Container):
            raise Exception(f"{other} must be of type Container")
        return MultiContainer([self, other])

    def __or__(self, other):
        """
        Examples:
            >>> Generic | Infinite
        """
        return self + other

    def __getitem__(self, item):
        """
        Examples:
            >>> Missing[Generic]
        """
        return item + self


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

    def __str__(cls) -> str:
        return f"{cls.__class__.__name__}"


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

    def __str__(self):
        return f"({', '.join([str(container.__class__) for container in self.containers])})"

    def __repr__(self):
        return str(self)


class Generic(Container):
    def mask(self, series):
        return np.ones((len(series),), dtype=np.bool)

    def contains_op(self, series):
        return True


class TypeC(Container):
    def __init__(self, base_type):
        self.base_type = base_type

    def mask(self, series):
        # TODO: exclude inf
        return series.notnull()

    def contains_op(self, series):
        return series[self.mask(series)] in self.base_type

    def __getitem__(self, item):
        self.base_type = item
        return self

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}[{self.base_type}]"


class Infinite(Container):
    """Allow missing values on type (e.g. np.nan, "NAN")

    Examples:
        >>> series =  pd.Series([1, 2, 3, np.nan, np.nan], name='lost')
        >>> series in missing
        True
    """

    def mask(self, series: pd.Series) -> pd.Series:
        """Get the ids containing missing values
         Args:
             series: Series to mask
         Returns:
             ids of the series that are missing.
         """
        return (~np.isfinite(series)) & series.notnull()

    def contains_op(self, series: pd.Series, mask=[]) -> bool:
        """Check if the series contains missing values
        Args:
            series: Series to check
        Returns:
            True if series contains at least one missing value.
        """
        return self.mask(series).any()


class Missing(Container):
    """Allow infinite values on type (e.g. np.inf)

    Examples:
        >>> series =  pd.Series([1, 2, 3, np.inf, -np.inf], name='infinity_on_trail')
        >>> series in infinite
        True
    """

    def mask(self, series: pd.Series) -> pd.Series:
        """Get the ids containing infinity values
        Args:
            series: Series to mask
        Returns:
            ids of the series that are infinite.
        """
        return series.isna()

    def contains_op(self, series: pd.Series, mask=[]) -> bool:
        """Check if the series contains infinite values
        Args:
            series: Series to check
        Returns:
            True if series contains at least one infinite value.
        """
        return series.hasnans


generic = Generic()
infinite = Infinite()
missing = Missing()
type = TypeC(tenzing_generic)
