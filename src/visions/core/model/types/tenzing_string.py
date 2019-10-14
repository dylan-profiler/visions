import pandas as pd
import pandas.api.types as pdt

from visions.core.model.model_relation import relation_conf
from visions.core.model.models import tenzing_model


class tenzing_string(tenzing_model):
    """**String** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series(['rubin', 'carter', 'champion'])
    >>> x in tenzing_string
    True
    """

    @classmethod
    def get_relations(cls):
        from visions.core.model.types import tenzing_object

        relations = {tenzing_object: relation_conf(inferential=False)}
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        # TODO: without the object check this passes string categories... is there a better way?
        if not pdt.is_object_dtype(series):
            return False
        elif series.hasnans:
            series = series.dropna()
            if series.empty:
                return False

        return all(type(v) is str for v in series)
