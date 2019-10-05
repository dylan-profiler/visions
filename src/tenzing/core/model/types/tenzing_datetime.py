import pandas.api.types as pdt
import pandas as pd

from tenzing.core.model.model_relation import relation_conf
from tenzing.core.model.models import tenzing_model
from tenzing.core.model.types import tenzing_string, tenzing_integer
from tenzing.utils.coercion import test_utils


def to_datetime(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series)


class tenzing_datetime(tenzing_model):
    """**Datetime** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series([pd.datetime(2017, 3, 5), pd.datetime(2019, 12, 4)])
    >>> x in tenzing_datetime
    True
    """

    @classmethod
    def get_relations(cls):
        from tenzing.core.model.types import tenzing_generic

        relations = {
            tenzing_generic: relation_conf(inferential=False),
            tenzing_string: relation_conf(
                relationship=test_utils.coercion_test(lambda s: pd.to_datetime(s)),
                transformer=to_datetime,
                inferential=True,
            ),
            # TODO: make sure that exception is raised before 1970-1-1 00:00:00
            # TODO: make contrib
            # tenzing_integer: relation_conf(
            #     inferential=True,
            #     relationship=test_utils.coercion_test(lambda s: pd.to_datetime(s.astype(str))),
            #     transformer=to_datetime,
            # )
        }
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_datetime64_any_dtype(series)
