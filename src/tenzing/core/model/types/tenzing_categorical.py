import pandas.api.types as pdt
import pandas as pd

from tenzing.core.model.model_relation import relation_conf
from tenzing.core.model.models import tenzing_model


class tenzing_categorical(tenzing_model):
    """**Categorical** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series([True, False, 1], dtype='category')
    >>> x in tenzing_categorical
    True
    """

    @classmethod
    def get_relations(cls) -> dict:
        from tenzing.core.model.types import tenzing_generic

        return {
            tenzing_generic: relation_conf(inferential=False),
        }

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_categorical_dtype(series)

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return series.astype("category")
