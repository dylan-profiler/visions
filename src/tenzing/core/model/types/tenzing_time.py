import pandas.api.types as pdt
import pandas as pd

from tenzing.core.model.model_relation import relation_conf
from tenzing.core.model.models import tenzing_model


class tenzing_time(tenzing_model):
    """**Time** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series([pd.datetime(2017, 3, 5), pd.datetime(2019, 12, 4)])
    >>> x in tenzing_time
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
        # Substantially better scaling
        if not pdt.is_datetime64_any_dtype(series):
            return False

        temp_series = series.dropna()
        return all(
            (
                temp_series.dt.day.eq(1).all(),
                temp_series.dt.month.eq(1).all(),
                temp_series.dt.year.eq(1970).all(),
            )
        )
