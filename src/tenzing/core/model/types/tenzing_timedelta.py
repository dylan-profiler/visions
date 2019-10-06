import pandas.api.types as pdt
import pandas as pd

from tenzing.core.model.model_relation import relation_conf
from tenzing.core.model.models import tenzing_model


class tenzing_timedelta(tenzing_model):
    """**Timedelta** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series([pd.Timedelta(days=i) for i in range(3)])
    >>> x in tenzing_timedelta
    True
    """

    @classmethod
    def get_relations(cls):
        from tenzing.core.model.types import tenzing_generic

        relations = {tenzing_generic: relation_conf(inferential=False)}
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_timedelta64_dtype(series)
