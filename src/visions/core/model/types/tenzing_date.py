import pandas as pd
import pandas.api.types as pdt

from visions.core.model.model_relation import relation_conf
from visions.core.model.models import tenzing_model


class tenzing_date(tenzing_model):
    """**Date** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series([pd.datetime(2017, 3, 5), pd.datetime(2019, 12, 4)])
    >>> x in tenzing_date
    True
    """

    @classmethod
    def get_relations(cls):
        from visions.core.model.types import tenzing_datetime

        relations = {tenzing_datetime: relation_conf(inferential=False)}
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        if not pdt.is_datetime64_any_dtype(series):
            return False

        temp_series = series.dropna().dt
        time_val_map = {'hour': 0, 'minute': 0, 'second': 0}
        return all(getattr(temp_series, time_part).eq(val).all() for time_part, val in time_val_map.items())
