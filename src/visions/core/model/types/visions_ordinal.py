import pandas.api.types as pdt
import pandas as pd

from visions.core.model.model_relation import relation_conf
from visions.core.model.models import VisionsBaseType


def to_ordinal(series: pd.Series) -> pd.Series:
    return pd.Series(
        pd.Categorical(series, categories=sorted(series.unique()), ordered=True)
    )


class visions_ordinal(VisionsBaseType):
    """**Ordinal** implementation of :class:`visions.core.models.VisionsBaseType`.
    >>> x = pd.Series([1, 2, 3, 1, 1], dtype='category')
    >>> x in visions_ordinal
    True
    """

    @classmethod
    def get_relations(cls):
        from visions.core.model.types import visions_categorical

        relations = {visions_categorical: relation_conf(inferential=False)}
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_categorical_dtype(series) and series.cat.ordered
