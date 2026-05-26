import pandas as pd

from visions.backends.pandas.series_utils import pandas_is_categorical, series_not_empty
from visions.types.ordinal import Ordinal

# @Ordinal.register_transformer(Categorical, pd.Series)
# def categorical_to_ordinal(series: pd.Series) -> pd.Categorical:
#     return pd.Categorical(
#         series, categories=sorted(series.dropna().unique()), ordered=True
#     )


@Ordinal.contains_op.register
@series_not_empty
def ordinal_contains(series: pd.Series, state: dict) -> bool:
    return pandas_is_categorical(series) and series.cat.ordered
