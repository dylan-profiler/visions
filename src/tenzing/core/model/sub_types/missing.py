import pandas as pd
from tenzing.core.model.sub_type import subType


class missing(subType):
    """Allow missing values on type (e.g. np.nan, "NAN")

    >>> series =  pd.Series([1, 2, 3, np.nan, np.nan], name='lost')
    >>> series in missing
    True
    """

    @staticmethod
    def get_mask(series: pd.Series) -> bool:
        """Get the ids containing missing values

        Args:
            series: Series to mask

        Returns:
            ids of the series that are missing.
        """
        return series.isna()

    @staticmethod
    def contains_op(series: pd.Series) -> bool:
        """Check if the series contains missing values

        Args:
            series: Series to check

        Returns:
            True if series contains at least one missing value.
        """
        return series.hasnans
