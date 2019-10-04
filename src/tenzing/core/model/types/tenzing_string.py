import pandas as pd
import pandas.api.types as pdt

from tenzing.core.model.model_relation import relation_conf
from tenzing.core.model.models import tenzing_model


class tenzing_string(tenzing_model):
    """**String** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series(['rubin', 'carter', 'champion'])
    >>> x in tenzing_string
    True
    """

    @classmethod
    def register_relations(cls):
        from tenzing.core.model.types import tenzing_generic

        relations = {
            tenzing_generic: relation_conf(inferential=False)
        }
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        # TODO: without the object check this passes string categories... is there a better way?
        return (
            pdt.is_object_dtype(series) & series[series.notna()].map(type).eq(str).all()
        )

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return series.astype(str)
