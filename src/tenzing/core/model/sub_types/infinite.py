import numpy as np
import pandas as pd

from tenzing.core.model.sub_type import subType


class infinite(subType):
    """Allow infinite values on type (e.g. np.inf)

    >>> series =  pd.Series([1, 2, 3, np.inf, -np.inf], name='infinity_on_trail')
    >>> series in infinite
    True
    """

    @staticmethod
    def get_mask(series: pd.Series) -> bool:
        """Get the ids containing infinity values

        Args:
            series: Series to mask

        Returns:
            ids of the series that are infinite.
        """
        return (~np.isfinite(series)) & series.notnull()

    @staticmethod
    def contains_op(series: pd.Series) -> bool:
        """Check if the series contains infinite values

        Args:
            series: Series to check

        Returns:
            True if series contains at least one infinite value.
        """
        return ((~np.isfinite(series)) & series.notnull()).any()
