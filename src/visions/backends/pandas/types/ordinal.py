import pandas as pd
from pandas.api import types as pdt

from visions.backends.pandas.series_utils import series_not_empty
from visions.types.ordinal import ordinal_contains

# def to_ordinal(series: pd.Series) -> pd.Categorical:
#     return pd.Categorical(
#         series, categories=sorted(series.dropna().unique()), ordered=True
#     )


@ordinal_contains.register(pd.Series)
@series_not_empty
def _(series: pd.Series, state: dict) -> bool:
    return pdt.is_categorical_dtype(series) and series.cat.ordered
