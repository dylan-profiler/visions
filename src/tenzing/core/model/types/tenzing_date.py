import pandas as pd
import pandas.api.types as pdt

from tenzing.core.model.model_relation import relation_conf
from tenzing.core.model.models import tenzing_model


class tenzing_date(tenzing_model):
    """**Date** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series([pd.datetime(2017, 3, 5), pd.datetime(2019, 12, 4)])
    >>> x in tenzing_date
    True
    """

    @classmethod
    def get_relations(cls):
        from tenzing.core.model.types import tenzing_datetime

        relations = {
            tenzing_datetime: relation_conf(inferential=False)
        }
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        if not pdt.is_datetime64_any_dtype(series):
            return False

        temp_series = series.dropna()
        return all(
            [
                temp_series.dt.hour.eq(0).all(),
                temp_series.dt.minute.eq(0).all(),
                temp_series.dt.second.eq(0).all(),
            ]
        )

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return pd.to_datetime(series)
