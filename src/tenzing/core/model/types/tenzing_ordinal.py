import pandas.api.types as pdt
import pandas as pd

from tenzing.core.model.model_relation import relation_conf
from tenzing.core.model.models import tenzing_model


def to_ordinal(series: pd.Series) -> pd.Series:
    return pd.Series(
        pd.Categorical(series, categories=sorted(series.unique()), ordered=True)
    )


class tenzing_ordinal(tenzing_model):
    """**Ordinal** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series([1, 2, 3, 1, 1], dtype='category')
    >>> x in tenzing_ordinal
    True
    """

    @classmethod
    def get_relations(cls):
        from tenzing.core.model.types import tenzing_categorical

        relations = {
            tenzing_categorical: relation_conf(inferential=False),
        }
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_categorical_dtype(series) and series.cat.ordered
